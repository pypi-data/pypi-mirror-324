from typing import List, Optional, Dict, Any, Tuple, Union
import random
import pandas as pd
import numpy as np
from tqdm import tqdm
import logging

import torch
from torch.utils.data import DataLoader
from torch.nn.functional import softmax
from transformers import DataCollatorWithPadding

from dreamml.modeling.models.estimators import BaseModel
from dreamml.utils.bert_utils import (
    TextDataset,
    load_model,
    load_tokenizer,
    unfreeze_model_layers,
    get_loss_function,
    get_optimizer,
    get_scheduler,
    get_sampler,
    move_to_device,
    EarlyStopping,
)

seed = 27
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)


class BertModel(BaseModel):
    """
    Bert Model для стейджей vectorization и opt.
    """

    model_name = "bert"

    def __init__(
        self,
        estimator_params: Dict[str, Any],
        task: str,
        used_features: List[str],
        categorical_features: List[str],
        metric_name,
        metric_params,
        parallelism: int = -1,
        train_logger: Optional[logging.Logger] = None,
        text_features=None,
        augmentation_params: Tuple[list, float] = None,
        **params,
    ):
        super().__init__(
            estimator_params,
            task,
            used_features,
            categorical_features,
            metric_name,
            metric_params,
            parallelism=parallelism,
            train_logger=train_logger,
            text_features=text_features,
            augmentation_params=augmentation_params,
            **params,
        )

        self.model_path = self.params["model_path"]
        self.tokenizer = load_tokenizer(self.model_path)
        self.loss_fn = get_loss_function(self.params["objective"])
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        self.num_labels: int = len(metric_params["labels"])
        self.model = load_model(self.model_path, self.num_labels)
        self.model = unfreeze_model_layers(self.model, self.params["unfreeze_layers"])
        self.vector_size = self.model.config.hidden_size
        self.used_features = [f"{self.model_name}_{i}" for i in range(self.vector_size)]

        if self.params["max_length"] is None:
            self.params["max_length"] = self.tokenizer.model_max_length
        self._logger.info(f"Bert params: {self.params}")

    def fit(self, data, target, *eval_set):

        # Для Берта конкатенируем все text_features
        valid_data, valid_target = eval_set
        train_concat_features = (
            data[self.text_features].astype(str).agg(" ".join, axis=1)
        )
        valid_concat_features = (
            valid_data[self.text_features].astype(str).agg(" ".join, axis=1)
        )

        train_loader = self._get_sample_loader(
            train_concat_features,
            target,
            self.params["sampler_type"],
            self.text_augmentations,
            self.aug_p,
        )
        valid_loader = self._get_sample_loader(
            valid_concat_features, target, "sequential"
        )

        self._train_model(train_loader, valid_loader)

    def _train_model(self, train_loader, valid_loader):
        total_steps = len(train_loader) * self.params["epochs"]
        gradient_accumulation_steps = max(1, 32 // self.params["batch_size"])
        gradient_accumulation_steps = 1  # test
        early_stopping = EarlyStopping(patience=2, min_delta=0.001)

        optimizer = get_optimizer(
            self.model,
            self.params["learning_rate"],
            self.params["optimizer_type"],
            self.params["weight_decay"],
        )
        scheduler = get_scheduler(
            optimizer,
            self.params["scheduler_type"],
            self.params["optimizer_type"],
            total_steps,
        )

        train_losses = []
        valid_losses = []

        for epoch in tqdm(
            range(self.params["epochs"]), desc="Fit epochs", position=0, leave=True
        ):
            self._logger.info(f"Epoch: {epoch + 1} / {self.params['epochs']}")

            train_losses, valid_losses, avg_valid_loss_per_epoch = (
                self._train_one_epoch(
                    train_loader,
                    valid_loader,
                    gradient_accumulation_steps,
                    optimizer,
                    scheduler,
                    train_losses,
                    valid_losses,
                )
            )
            # Check early stopping
            early_stopping(avg_valid_loss_per_epoch)
            if early_stopping.early_stop:
                self._logger.info(f"Epoch {epoch} | Early stopping")
                break

    def _train_one_epoch(
        self,
        train_loader,
        valid_loader,
        gradient_accumulation_steps,
        optimizer,
        scheduler,
        train_losses,
        valid_losses,
    ):
        self.model.to(self.params["device"])

        # Training phase
        self.model.train()
        train_loss = 0

        for idx, batch in enumerate(
            tqdm(train_loader, desc="Fit", position=0, leave=True)
        ):
            optimizer.zero_grad()
            input_ids, attention_mask, labels = move_to_device(
                batch, self.params["device"]
            )
            outputs = self.model(
                input_ids=input_ids, attention_mask=attention_mask, labels=labels
            )
            loss = self.loss_fn(outputs.logits, labels)
            loss.backward()
            train_loss += loss.item()

            if idx % 50 == 0 or idx == len(train_loader):
                self._logger.info(f"Batch: {idx} / {len(train_loader)} | Loss: {loss}")

            if (idx + 1) % gradient_accumulation_steps == 0:
                optimizer.step()
                if self.params["scheduler_type"] == "reduce_on_plateau":
                    scheduler.step(loss)
                else:
                    scheduler.step()

        avg_train_loss = train_loss / len(train_loader)
        train_losses.append(avg_train_loss)

        # Validation phase
        self.model.eval()
        valid_loss = 0

        with torch.no_grad():
            for idx, batch in enumerate(
                tqdm(valid_loader, desc="Validate", position=0, leave=True)
            ):
                input_ids, attention_mask, labels = move_to_device(
                    batch, self.params["device"]
                )
                outputs = self.model(
                    input_ids=input_ids, attention_mask=attention_mask, labels=labels
                )
                loss = self.loss_fn(outputs.logits, labels)
                valid_loss += loss.item()

        avg_valid_loss = valid_loss / len(valid_loader)
        valid_losses.append(avg_valid_loss)
        self._logger.info(
            f"Epoch avg losses: Train: {avg_train_loss} | Valid: {avg_valid_loss}"
        )

        return train_losses, valid_losses, avg_valid_loss

    @torch.no_grad()
    def transform(
        self, data: pd.DataFrame, return_embedds=False
    ) -> Union[pd.DataFrame, np.array]:
        """
        :param data: Датафрейм признаков
        :param return_embedds: Флаг для возвращения датафрейма эмбеддингов

        :return:
            Если return_embedds = True - возвращается датафрейм эмбеддингов
            Если return_embedds = False - возвращается матрица скоров
        """
        probabilities_list, embeddings_list = [], []
        self.model.to(self.params["device"])
        self.model.eval()

        concat_features = data[self.text_features].astype(str).agg(" ".join, axis=1)
        loader = self._get_sample_loader(
            concat_features, target=None, sampler_type="sequential"
        )

        for idx, batch in enumerate(
            tqdm(loader, desc="Transform batches", position=0, leave=True)
        ):
            input_ids, attention_mask, _ = move_to_device(batch, self.params["device"])
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            embedding = outputs.hidden_states[-1].mean(dim=1).cpu().numpy()
            embeddings_list.append(embedding)
            probabilities = softmax(outputs.logits, dim=1).cpu().numpy()
            probabilities_list.append(probabilities)

        if return_embedds:
            embeddings_df = pd.DataFrame(
                data=np.concatenate(embeddings_list, axis=0),
                columns=self.used_features,
                index=data.index,
            )
            return embeddings_df

        predictions = np.concatenate(probabilities_list, axis=0)
        if self.task == "binary":
            return predictions[:, 1]
        elif self.task in ("multilabel", "multiclass"):
            return predictions
        else:
            return

    def _get_sample_loader(
        self,
        data,
        target: Optional[pd.Series] = None,
        sampler_type: str = "sequential",
        augmenters: Optional[list] = None,
        aug_p: float = 0.2,
    ):
        dataset = TextDataset(
            texts=data.tolist(),
            labels=None if target is None else target.tolist(),
            tokenizer=self.tokenizer,
            max_length=self.params["max_length"],
            augmenters=augmenters,
            aug_p=aug_p,
        )
        sampler = get_sampler(dataset, sampler_type, self.params["batch_size"])
        loader = DataLoader(
            dataset,
            batch_size=self.params["batch_size"],
            sampler=sampler,
            collate_fn=self.data_collator,
        )
        return loader