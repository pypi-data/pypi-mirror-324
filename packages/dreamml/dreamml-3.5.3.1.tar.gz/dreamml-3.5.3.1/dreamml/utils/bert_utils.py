from typing import Dict
import random

import torch
from torch import nn
from torch.optim import AdamW, Adam, SGD, RMSprop
from torch.optim.lr_scheduler import (
    ExponentialLR,
    StepLR,
    ReduceLROnPlateau,
    OneCycleLR,
    CyclicLR,
)
from torch.utils.data import (
    Dataset,
    RandomSampler,
    SequentialSampler,
    SubsetRandomSampler,
    WeightedRandomSampler,
    BatchSampler,
)
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_linear_schedule_with_warmup,
)

from dreamml.utils.make_weights_for_balanced_classes import (
    make_weights_for_balanced_classes,
)


class TextDataset(Dataset):
    def __init__(
        self,
        texts,
        labels=None,
        tokenizer=None,
        max_length=None,
        augmenters=None,
        aug_p=0.2,
    ):
        """
        :param texts: Список текстов
        :param labels: Список меток (опционально)
        :param tokenizer: Токенизатор
        :param max_length: Максимальная длина токенов
        :param augmenters: Список аугментаторов из библиотеки nlpaug (опционально)
        :param aug_p: Вероятность применения аугментации к тексту
        """
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.augmenters = augmenters or []
        self.aug_p = aug_p

        if self.augmenters:  # Генерация оригинальных и аугментированных текстов
            self.texts, self.labels = self._generate_augmented_texts(
                self.texts, self.labels
            )

        # Претокенизация всего датасета
        self.tokenized_texts = self._tokenize_texts(self.texts)

    def _apply_augmentations(self, text):
        """
        Применяет все аугментаторы к тексту, если они заданы.
        """
        augmented_texts = [text]
        if self.augmenters:
            for aug in self.augmenters:
                augmented_texts.extend(aug.augment(text))
        return augmented_texts

    def _generate_augmented_texts(self, texts, labels):
        """
        Генерирует список всех текстов и меток, включая оригинальные и аугментированные.
        """
        all_texts = []
        all_labels = []
        for text, label in zip(texts, labels):
            if random.random() < self.aug_p:
                augmented_texts = self._apply_augmentations(text)
                all_texts.append(text)  # Добавляем оригинальный текст
                all_labels.append(label)  # Добавляем метку для оригинального текста
                # Добавляем аугментированные тексты и повторяем метку для каждого
                all_texts.extend(augmented_texts)
                all_labels.extend([label] * len(augmented_texts))
            else:
                # Добавляем текст и метку без аугментации
                all_texts.append(text)
                all_labels.append(label)
        return all_texts, all_labels

    def _tokenize_texts(self, texts):
        """
        Токенизирует все тексты.
        """
        tokenized_texts = []
        for text in texts:
            encoding = self.tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_length,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                return_tensors="pt",
            )
            tokenized_texts.append(
                {
                    "input_ids": encoding["input_ids"].squeeze(0),
                    "attention_mask": encoding["attention_mask"].squeeze(0),
                }
            )
        return tokenized_texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        tokenized_data = self.tokenized_texts[idx]

        item = {
            "input_ids": tokenized_data["input_ids"],
            "attention_mask": tokenized_data["attention_mask"],
        }

        if self.labels is not None:
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)

        return item


# Сервисные функции для transformers.AutoModelForSequenceClassification
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def load_tokenizer(model_name_or_path: str):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    except:
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False)
    return tokenizer


def load_model(
    model_name_or_path: str, num_labels: int, output_hidden_states: bool = True
):
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name_or_path,
        num_labels=num_labels,
        output_hidden_states=output_hidden_states,
    )
    return model


def unfreeze_model_layers(model, unfreeze_layers: str = "all"):
    if unfreeze_layers == "classifier":
        for name, param in model.named_parameters():
            if "classifier" in name:
                param.requires_grad = True
            else:
                param.requires_grad = False

    if unfreeze_layers == "classifier_and_pooler":
        for name, param in model.named_parameters():
            if "classifier" in name or "pooler" in name:
                param.requires_grad = True
            else:
                param.requires_grad = False

    elif unfreeze_layers.startswith("last_"):
        n_layers = int(unfreeze_layers.split("_")[1])
        for name, param in model.named_parameters():
            if "classifier" in name or "pooler" in name:
                param.requires_grad = True

            elif "encoder.layer" in name:
                layer_num = int(name.split(".")[3])
                if layer_num >= 12 - n_layers:
                    param.requires_grad = True
                param.requires_grad = False
            else:
                param.requires_grad = False

    elif unfreeze_layers == "all":
        for param in model.parameters():
            param.requires_grad = True

    return model


def get_loss_function(loss_type: str):
    if loss_type == "logloss":
        return nn.CrossEntropyLoss()
    elif loss_type == "cross-entropy":
        return nn.CrossEntropyLoss()
    elif loss_type == "mse":
        return nn.MSELoss()
    elif loss_type == "bce":
        return nn.BCELoss()
    else:
        raise ValueError(f"Неизвестный тип функции потерь: {loss_type}")


def get_optimizer(model, learning_rate, optimizer_type: str, weight_decay: float):
    if optimizer_type == "adamw":
        return AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == "adam":
        return Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == "sgd":
        return SGD(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == "rmsprop":
        return RMSprop(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    else:
        raise ValueError(f"Неизвестный тип оптимизатора: {optimizer_type}")


def move_to_device(batch: Dict[str, torch.Tensor], device: str):
    input_ids = batch["input_ids"].to(device)
    attention_mask = batch["attention_mask"].to(device)
    labels = None
    if "labels" in batch:
        labels = batch["labels"].to(device)
    return input_ids, attention_mask, labels


def get_scheduler(
    optimizer, scheduler_type: str, optimizer_type: str, total_steps: int
):
    if scheduler_type == "linear":
        return get_linear_schedule_with_warmup(
            optimizer, num_warmup_steps=0, num_training_steps=total_steps
        )
    elif scheduler_type == "exponential":
        return ExponentialLR(optimizer, gamma=0.9)
    elif scheduler_type == "step":
        return StepLR(optimizer, step_size=10, gamma=0.1)
    elif scheduler_type == "reduce_on_plateau":
        return ReduceLROnPlateau(optimizer, mode="min", factor=0.1, patience=10)
    elif scheduler_type == "one_cycle_lr":
        return OneCycleLR(optimizer, max_lr=1e-3, total_steps=total_steps)
    elif scheduler_type == "cyclic_lr":
        if optimizer_type == "adamw" or optimizer_type == "adam":
            return CyclicLR(
                optimizer,
                base_lr=5e-5,
                max_lr=1e-3,
                step_size_up=5,
                cycle_momentum=False,
            )
        return CyclicLR(optimizer, base_lr=5e-5, max_lr=1e-3, step_size_up=5)
    else:
        raise ValueError(f"Неизвестный тип scheduler: {scheduler_type}")


def get_sampler(dataset: TextDataset, sampler_type: str, batch_size: int):
    if sampler_type == "random":
        return RandomSampler(dataset)
    elif sampler_type == "sequential":
        return SequentialSampler(dataset)
    elif sampler_type == "subset_random":
        indices = list(range(len(dataset)))
        return SubsetRandomSampler(indices)
    elif sampler_type == "weighted_random":
        weights = make_weights_for_balanced_classes(
            dataset.labels, len(set(dataset.labels))
        )
        weights = torch.DoubleTensor(weights)
        return WeightedRandomSampler(weights, len(weights))
    elif sampler_type == "batch":
        sampler = RandomSampler(dataset)
        return BatchSampler(sampler, batch_size=batch_size, drop_last=False)
    else:
        raise ValueError(f"Неизвестный тип сэмплера: {sampler_type}")


class EarlyStopping:
    def __init__(self, patience=2, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True