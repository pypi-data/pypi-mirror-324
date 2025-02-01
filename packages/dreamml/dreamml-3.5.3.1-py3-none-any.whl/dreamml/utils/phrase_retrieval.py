import os
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
from copy import deepcopy
import pandas as pd
import numpy as np
from nltk.tokenize import sent_tokenize
import torch
from sentence_transformers import SentenceTransformer
from dreamml.utils import sbertpunccase as sbert_punct
from dreamml.configs.config_storage import ConfigStorage
from dreamml.data._transformer import DataTransformer
from dreamml.logging import get_logger

tqdm.pandas(desc="Preprocessing")

BAD_PHRASES_PATH = Path(__file__).parent.parent / "references/bad_phrases_clean.csv"

_logger = get_logger(__name__)


class PhraseRetrieval:
    def __init__(self, config: Dict):
        """
        config: dict - словарь с параметрами.
        """
        self.config = config
        self.device = self.config.get(
            "device", "cuda:0" if torch.cuda.is_available() else "cpu"
        )
        self.e5_model = SentenceTransformer(
            self.config["e5_model_path"], device=self.device
        )

        if self.config.get("punct_model_repo"):
            sbert_punct.MODEL_REPO = self.config["punct_model_repo"]
            self.punct_model = sbert_punct.SbertPuncCase().to(self.device)
        else:
            self.punct_model = None

    def load_datasets(self):
        """Метод для загрузки датасетов с файловой системы или Hadoop."""

        task = self.config.get("task", "phrase_retrieval")
        dialog_id_col = self.config.get("dialog_id_col", "dialog_id")
        text_col = self.config.get("text_col", "PraseText")
        phrase_col = self.config.get("phrase_col", "Фраза")

        dialog_path = self.config["dialog_path"]
        bad_phrases_path = self.config.get("bad_phrases_path", None)

        if bad_phrases_path is None:
            bad_phrases_path = str(BAD_PHRASES_PATH)

        config = {
            "task": task,
            "dev_data_path": dialog_path,
            "oot_data_path": bad_phrases_path,
        }
        config_storage = ConfigStorage(config)
        transformer = DataTransformer(config_storage)
        data_dict = transformer._get_data()

        self.data = data_dict["dev"][[dialog_id_col, text_col]]
        self.data.columns = ["dialog_id", "text"]
        self.bad_phrases = data_dict["oot"][phrase_col].tolist()

    def restore_punctuation(self):
        """Восстанавливаем пунктуацию, если модель указана."""
        if self.punct_model:
            self.data["punct_text"] = self.data["text"].progress_apply(
                lambda x: self.punct_model.punctuate(x)
            )
        else:
            self.data["punct_text"] = self.data[
                "text"
            ]  # Если модель пунктуации не указана, используем оригинальный текст

    def text_to_sentences_df(self, min_length) -> pd.DataFrame:
        """Разбиение текста на предложения и объединение коротких предложений."""
        sent_tokenize_lang = self.config.get("sent_tokenize_lang", "russian")
        all_sents = (
            self.data["punct_text"]
            .progress_apply(
                lambda x: [s for s in sent_tokenize(x, language=sent_tokenize_lang)]
            )
            .to_list()
        )
        all_sents = [
            self.merge_short_sentences(dialog_sents, min_length)
            for dialog_sents in all_sents
        ]

        lengths = [len(sents) for sents in all_sents]
        d_ids = [
            d_id for (d_id, l) in zip(self.data["dialog_id"], lengths) for i in range(l)
        ]

        all_sents = [sent for sents in all_sents for sent in sents]  # Flatten
        return pd.DataFrame({"dialog_id": d_ids, "sentence": all_sents})

    @staticmethod
    def merge_short_sentences(sentences: List[str], min_length: int) -> List[str]:
        """Объединяем короткие предложения."""
        merged_sents = []
        i = 0

        while i < len(sentences):
            s = sentences[i]
            if len(s) >= min_length:
                merged_sents.append(s)
                i += 1
                continue
            while len(s) < min_length and i < len(sentences) - 1:
                s += " " + sentences[i + 1]
                i += 1
            merged_sents.append(s)
            i += 1
        return merged_sents

    def get_query_embs(self, phrases: List[str], batch_size: int = 64) -> np.ndarray:
        """Получаем эмбеддинги для фраз."""
        return self.e5_model.encode(
            ["query: " + s for s in phrases], batch_size=batch_size
        )

    def get_scores(
        self, all_sents: List[str], ph_embs: np.ndarray, batch_size: int = 512
    ) -> np.ndarray:
        """Вычисляем косинусную близость между предложениями и эмбеддингами фраз."""
        return (
            self.e5_model.encode(
                ["query: " + s for s in all_sents], batch_size=batch_size
            )
            @ ph_embs.T
        )

    def phrases_retrieve(
        self, sents_df: pd.DataFrame, scores: pd.DataFrame, threshold: float = 0.9
    ) -> pd.DataFrame:
        """Ищем предложения, которые похожи на плохие фразы."""
        result_df = pd.DataFrame()
        for phrase in tqdm(self.bad_phrases, desc="Phrase"):
            top_scores = scores.loc[scores[phrase] > threshold, phrase]
            tmp = sents_df.loc[top_scores.index]
            tmp["score"] = top_scores
            tmp["phrase"] = phrase
            result_df = pd.concat([result_df, tmp])
        return result_df

    def fit(self):
        """Загружаем данные и восстанавливаем пунктуацию, если указана модель."""
        self.load_datasets()
        self.restore_punctuation()

    def transform(
        self,
        threshold: float = None,
        min_length: int = None,
        batch_size_phrases: int = None,
        batch_size_dialogs: int = None,
    ) -> pd.DataFrame:
        """Преобразуем текст в эмбеддинги и ищем совпадения с плохими фразами."""

        threshold = (
            self.config.get("threshold", 0.9) if threshold is None else threshold
        )
        min_length = (
            self.config.get("min_length", 20) if min_length is None else min_length
        )
        batch_size_phrases = (
            self.config.get("batch_size_phrases", 512)
            if batch_size_phrases is None
            else batch_size_phrases
        )
        batch_size_dialogs = (
            self.config.get("batch_size_dialogs", 64)
            if batch_size_dialogs is None
            else batch_size_dialogs
        )

        all_sents_df = self.text_to_sentences_df(min_length=min_length)
        phrases_embs = self.get_query_embs(
            self.bad_phrases, batch_size=batch_size_phrases
        )

        # Вычисление косинусной близости
        scores = pd.DataFrame(
            self.get_scores(
                all_sents_df["sentence"].tolist(),
                phrases_embs,
                batch_size=batch_size_dialogs,
            )
        )
        scores.columns = self.bad_phrases

        # Поиск предложений, содержащих плохие фразы
        self.result_df = self.phrases_retrieve(
            all_sents_df, scores, threshold=threshold
        )

        params = {
            "threshold": threshold,
            "min_length": min_length,
            "batch_size_phrases": batch_size_phrases,
            "batch_size_dialogs": batch_size_dialogs,
        }

        _logger.debug(f"Phrase Retrieval config: {self.config}")
        _logger.debug(f"Transform params: {params}")

        return self.result_df

    def get_top_dialogs(self, top_n: int = 10, unique=True):
        result_df = deepcopy(self.result_df)

        result_df.sort_values(by="score", ascending=False, inplace=True)
        result_df.reset_index(drop=True, inplace=True)

        if unique:
            result_df.drop_duplicates(subset=["dialog_id"], keep="first", inplace=True)
            top_unique_dialogs = result_df["dialog_id"].head(top_n)
            result_df = result_df[result_df["dialog_id"].isin(top_unique_dialogs)]
        else:
            result_df = result_df.head(n=top_n)

        return result_df