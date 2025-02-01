from nlpaug.augmenter.word import WordAugmenter

from typing import List, Dict
import random


class SynonymsWordAug(WordAugmenter):

    def __init__(
        self,
        name="SynonymsWordAug",
        aug_min=1,
        aug_max=None,
        aug_p=0.3,
        stopwords=None,
        tokenizer=None,
        reverse_tokenizer=None,
        device="cpu",
        verbose=0,
        stopwords_regex=None,
        custom_synonyms: Dict[str, List[str]] = dict(),
    ):
        super(SynonymsWordAug, self).__init__(
            action="substitute",
            name=name,
            aug_min=aug_min,
            aug_max=aug_max,
            aug_p=aug_p,
            stopwords=stopwords,
            tokenizer=tokenizer,
            reverse_tokenizer=reverse_tokenizer,
            device=device,
            verbose=0,
            stopwords_regex=stopwords_regex,
        )

        self.custom_synonyms: Dict[str, List[str]] = custom_synonyms

    def _detect_language(self, word):
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

    def _transform(self, token: str) -> str:
        synonyms: list = []
        synonyms.extend(self.custom_synonyms.get(token), [])
        if not len(synonyms):
            return token

        return random.choice(synonyms)

    def substitute(self, data):
        """
        :param tokens: list of token
        :return: list of token
        """
        tokens = self.tokenizer(data)
        results = tokens.copy()

        aug_idexes = self._get_random_aug_idxes(tokens)
        if aug_idexes is None:
            return data
        aug_idexes.sort(reverse=True)

        for aug_idx in aug_idexes:
            new_word = self._transform(results[aug_idx])
            results[aug_idx] = new_word

        return self.reverse_tokenizer(results)