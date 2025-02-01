import os
import re
from copy import deepcopy
from pathlib import Path
from tqdm.auto import tqdm
from yaml import load, FullLoader
from collections import Counter
from multiprocessing import Pool
from itertools import chain
from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from natasha import (
    Segmenter,
    MorphVocab,
    NewsMorphTagger,
    Doc,
    NewsEmbedding,
    NewsNERTagger,
)
from dreamml.logging import get_logger


tqdm.pandas()

_logger = get_logger(__name__)


SYNONYMOS_DATA_PATH = Path(__file__).parent.parent.parent / "references/synonyms.yaml"
SUPPORTED_PREPROCESSING_STAGES = [
    "remove_stopwords",
    "augmentation",
    "anonimization",
    "drop_unlikely_words",
    "lemmatization",
]


class CounterTransformer:
    stopwords = stopwords.words("english") + stopwords.words("russian")

    def __init__(self):
        self.fitted = False

    def fit(self, data: List[List[str]]):
        self.counts = Counter([v for t in data for v in t])
        self.fitted = True

    def transform(self, data: List[List[str]], threshold: int = 1) -> List[List[str]]:
        new_tokens = []
        for sample in data:
            sample_list = []
            for token in sample:
                if (
                    threshold is not None and self.counts[token] > threshold
                ) and token not in self.stopwords:
                    sample_list.append(token)
            new_tokens.append(sample_list)
        return new_tokens


class DropRareWordsTransformer:
    def __init__(self, min_occurences: int = 2, save_new_word: bool = True):
        self.fitted = False
        self.min_occurences = min_occurences
        self.new_word_occurences = (
            min_occurences if save_new_word else min_occurences - 1
        )
        self.word_counter = None

    def _check_is_fitted(self):
        if self.fitted and self.word_counter is not None:
            return True
        return False

    def _tokenize_text(self, text: str):
        return word_tokenize(text)

    def _filter_words(self, text):
        tokens = []
        for word in self._tokenize_text(text):
            if (
                self.word_counter.get(word, self.new_word_occurences)
                >= self.min_occurences
            ):
                tokens.append(word)
        tokens = " " if len(tokens) == 0 else tokens
        result = " ".join(tokens)
        return result

    def fit(self, text_feature: pd.Series):
        if self._check_is_fitted():
            pass
        else:
            with Pool() as pool:
                words_list = pool.map(self._tokenize_text, text_feature)
            self.word_counter = Counter(chain.from_iterable(words_list))
            self.fitted = True

    def transform(self, text_feature: pd.Series):
        with Pool() as pool:
            result = pool.map(self._filter_words, [text for text in text_feature])
        return result


class TextFeaturesTransformer:

    # FIXME: нет причины использовать здесь dict, нужно выписать как отдельные аргументы
    def __init__(self, config: dict):
        self.text_preprocessing_stages: List[str] = config["text_preprocessing_stages"]
        self.text_features = config["text_features"]
        self.text_features_preprocessed = []
        self.drop_features = config["drop_features"]
        self.augs = config["augs"]
        self.aug_p = config["aug_p"]
        self.indexes = config["indexes"]
        self.bert_anonimization = config["bert_anonimization"]
        self.stop_words_ru = set(stopwords.words("russian"))
        self.stop_words_en = set(stopwords.words("english"))
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_vocab = MorphVocab()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.lemmatizer_en = WordNetLemmatizer()
        self.synonyms_path_list = SYNONYMOS_DATA_PATH
        self.rare_class = DropRareWordsTransformer()
        self.preprocess_stages = []

        if os.path.exists(self.synonyms_path_list):
            with open(self.synonyms_path_list) as f:
                self.synonyms_dict: Dict[str, List[str]] = load(f, FullLoader)
        else:
            self.synonyms_dict: Dict[str, List[str]] = dict()

    def fit(self, data: pd.DataFrame):
        for stage_name in self.text_preprocessing_stages:
            if stage_name not in SUPPORTED_PREPROCESSING_STAGES:
                msg = f"Stage: {stage_name} is not supported. {SUPPORTED_PREPROCESSING_STAGES}."
                raise ValueError(msg)

        # FIXME: в чем смысл, если тоже самое есть в `transform`?
        _ = self._copy_new_features(data=data)

        # FIXME: следующий код должен исполняться при инициализации, так как от входных данных не зависит
        for idx, stage_name in enumerate(self.text_preprocessing_stages):
            if stage_name in ["anonimization", "remove_stopwords"]:
                self.preprocess_stages.append(stage_name)
        self.text_preprocessing_stages = [
            stage
            for stage in self.text_preprocessing_stages
            if stage not in self.preprocess_stages
        ]

    def transform(self, data: pd.DataFrame, apply_augs_flag: bool = False):
        data = self._copy_new_features(data=data)

        indexes = deepcopy(self.indexes)
        train_indexes = (
            indexes[0].tolist() if isinstance(indexes[0], pd.Index) else indexes[0]
        )

        # FIXME: далее очень много раз токенизируется текст и восстанавливается обратно, нужно оптимизировать
        for feature in self.text_features_preprocessed:

            # Сначала выполняются стейджи: ["remove_stopwords", "anonimization"]
            # В том порядке, который указал пользователь
            if len(self.preprocess_stages) != 0:
                _logger.info(
                    f"Preprocessing info: feature: {feature} ~~~ {self.preprocess_stages}"
                )

                data[feature] = data[feature].progress_apply(
                    lambda row: self._text_preprocessing(row, self.preprocess_stages)
                )

            # А после остальные: ["augmentation", "drop_unlikely_words", "lemmatization"]
            # В том порядке, который указал пользователь
            for stage_name in self.text_preprocessing_stages:
                _logger.info(f"Preprocessing info: feature: {feature} ~~~ {stage_name}")

                if (
                    stage_name == "augmentation"
                    and apply_augs_flag
                    and "_group_nlp_aug_field" not in data.columns
                ):
                    max_index = max([max(s) for s in self.indexes])
                    _sample, train_indexes = self._apply_augmentation(
                        data.iloc[train_indexes], max_index=max_index
                    )  # Переписать чтобы метод принимал одну фичу
                    data["_group_nlp_aug_field"] = data.index.tolist()
                    data = pd.concat([data, _sample], axis=0)
                    indexes[0].append(train_indexes)

                elif stage_name == "drop_unlikely_words":
                    data[feature] = self.drop_unlikely_words(data[feature])

                elif stage_name == "lemmatization":
                    data[feature] = data[feature].progress_apply(
                        self._apply_lemmatization
                    )

        return data, tuple(indexes)

    def _text_preprocessing(self, row: str, stage_list: List[str]) -> str:
        """
        1. Удаление чисел
        1. Удаление стоп-слов
        2. Замена email на токен "EMAILTOKEN"
        3. Замена аббервиатур компаний на токен "ABRCOMPANYTOKEN"
        4. Замена ссылок на токен "URLTOKEN"
        5. Удаление знаков препинания и других "лишних" символов
        6. Удаление лишних пробелов
        """

        tokens = word_tokenize(row)
        language = "ru" if len(tokens) == 0 else self.detect_language(tokens[0])

        for stage_name in stage_list:
            if stage_name == "remove_stopwords":
                tokens = self._remove_stopwords(tokens, language)

            elif stage_name == "anonimization":
                tokens = self._apply_anonimization(tokens, language)

        text = " ".join(tokens)
        text = self._remove_spec_chars(text)
        return text

    def _remove_stopwords(self, tokens: list, language: str):
        stopwords_list = self.stop_words_ru if language == "ru" else self.stop_words_en
        tokens = [token for token in tokens if token.lower() not in stopwords_list]

        return tokens

    def _apply_anonimization(self, tokens: list, language: str) -> list:
        tokens_list = []
        for token in tokens:
            token = self.numbers_processing(token)
            if language == "ru":
                token = self.email_processing(token)
                token = self.abr_company_processing(token)
                token = self.site_links_processing(token)
                tokens_list.append(token)
            else:
                token = self.email_processing(token)
                token = self.site_links_processing(token)
                tokens_list.append(token)
        return tokens_list

    def _remove_spec_chars(self, sentence: str) -> str:
        sentence = re.sub(r"[^a-zA-Za-яА-Я0-9\s]", "", sentence)
        sentence = re.sub(r"\s+", " ", sentence).strip()
        return sentence

    def _apply_lemmatization(self, row: str) -> str:
        """
        1. Лемматизация текста
        2. Анонимизация имен и локаций
        """
        tokens = word_tokenize(row)
        language = "ru" if len(tokens) == 0 else self.detect_language(tokens[0])
        text = []

        if language == "ru":
            doc = Doc(row)
            doc.segment(self.segmenter)
            doc.tag_morph(self.morph_tagger)
            doc.tag_ner(self.ner_tagger)

            for token in doc.tokens:
                if token.text in [
                    item.text for item in doc.spans if item.type == "PER"
                ]:
                    lem_token = "NAMETOKEN"
                elif token.text in [
                    item.text for item in doc.spans if item.type == "LOC"
                ]:
                    lem_token = "LOCATIONTOKEN"
                else:
                    lem_token = token.text
                    if not self.bert_anonimization:
                        token.lemmatize(self.morph_vocab)
                        lem_token = token.lemma

                text.append(lem_token)
        else:
            if self.bert_anonimization:
                text.append(row)
            else:
                # FIXME: WordNetLemmatizer почти бесоплезен без указания части речи
                # FIXME: сюда нужно подавать токены, а не текст
                tmp = self.lemmatizer_en.lemmatize(row)
                text.append(tmp)

        text = " " if len(text) == 0 else " ".join(text)

        return text

    def _apply_augmentation(
        self, train_data: pd.DataFrame, max_index: int
    ) -> Tuple[pd.DataFrame, pd.Index]:
        """
        Функция применяет аугментации из конфига на train_dataset для доли aug_p

        Parameters
        ----------
        train_data: pandas.core.frame.DataFrame
            Трейн выборка.

        max_index: int
            максимальный индекс тренировочной выборки

        Returns
        -------
        augs_data: pandas.core.frame.DataFrane
            Аугментированные данные

        indexes: List[int]
            Новые аугментированные train индексы
        """

        augs_data = []
        for aug in self.augs:
            data = train_data.sample(frac=self.aug_p).copy()
            for idx, text_feature in enumerate(self.text_features_preprocessed):
                data.loc[:, text_feature] = data.loc[:, text_feature].apply(
                    lambda row: self._augment(aug, row)
                )

            left_border, right_border = (max_index + 1), (max_index + 1 + len(data))
            _index = np.arange(left_border, right_border)
            max_index += len(data)
            augs_data.append(
                data.set_index(_index).assign(_group_nlp_aug_field=data.index.tolist())
            )

        augs_data = pd.concat(augs_data, axis=0)
        indexes = augs_data.index
        return augs_data, indexes

    # --------------------- Сервисные функции ---------------------

    def detect_language(self, word):
        english_letters = set("abcdefghijklmnopqrstuvwxyz")
        russian_letters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

        is_en = any(letter in english_letters for letter in word.lower())
        is_ru = any(letter in russian_letters for letter in word.lower())

        if is_en and not is_ru:
            return "en"
        elif is_ru and not is_en:
            return "ru"
        else:
            return "ru"

    def _augment(self, aug, row):
        augmented = aug.augment(row)
        if len(augmented):
            return augmented[0]
        return " ".join(row)

    def drop_unlikely_words(self, text_feature: pd.Series):
        self.rare_class.fit(text_feature)
        return self.rare_class.transform(text_feature)

    def numbers_processing(self, token: str) -> str:
        return re.sub(r"[0-9]", "", token)

    @staticmethod
    def email_processing(token: str) -> str:
        email_detector = "@"
        if email_detector in token:
            return "EMAILTOKEN"
        else:
            return token

    @staticmethod
    def abr_company_processing(token: str) -> str:
        company_detector = ["ооо", "оао", "пао", "тоо", "зао", "ип"]
        if token.lower() in company_detector:
            return "ABRCOMPANYTOKEN"
        else:
            return token

    @staticmethod
    def site_links_processing(token: str) -> str:
        link_re = re.compile(
            r"""\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|
                           (?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4})
                            {1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:
                            (?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9])
                            {0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|
                            (?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"""
        )
        if link_re.search(token):
            return "URLTOKEN"
        else:
            return token

    def _copy_new_features(self, data: pd.DataFrame):
        for feature in self.text_features:
            new_feature_name = f"{feature}_preprocessed"
            if new_feature_name not in self.text_features_preprocessed:
                self.text_features_preprocessed.append(new_feature_name)
            if new_feature_name not in data.columns:
                data[new_feature_name] = data[feature].copy()
        return data