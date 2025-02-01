import nlpaug.augmenter.char as nac
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
import nlpaug.augmenter.spectrogram as nsp
from nltk.tokenize import word_tokenize


class AugmentationWrapper:
    def __init__(self, aug_type, **kwargs):
        self.aug_type = aug_type
        self.params = kwargs

    @staticmethod
    def split(x):
        return word_tokenize(x)

    def _get_aug_type(self):
        if self.aug_type == "KeyboardAug":
            aug = nac.KeyboardAug(tokenizer=self.split, **self.params)
        elif self.aug_type == "RandomCharAug":
            aug = nac.RandomCharAug(tokenizer=self.split, **self.params)
        elif self.aug_type == "RandomWordAug":
            aug = naw.RandomWordAug(**self.params)
        elif self.aug_type == "SplitAug":
            aug = naw.SplitAug(**self.params)
        elif self.aug_type == "OCR":
            aug = nac.OcrAug(tokenizer=self.split, **self.params)

        # Работает для lang='eng'
        # Для lang='rus' не нашел файла в nltk_data
        elif self.aug_type == "SynonymAug":
            aug = naw.SynonymAug(**self.params)
        elif self.aug_type == "BackTranslationAug":
            aug = naw.BackTranslationAug(**self.params)

        else:
            raise ValueError(f"Unknown augmentation type: {self.aug_type}")
        return aug

    def augment(self, text):
        aug = self._get_aug_type()
        return aug.augment(text)