from copy import deepcopy
from typing import Optional, Dict

import pandas as pd

from dreamml.configs.config_storage import ConfigStorage
from dreamml.logging import get_logger
from dreamml.modeling.models.estimators._lightautoml import LAMA

_logger = get_logger(__name__)


def add_lama_model(
    data: dict,
    config: ConfigStorage,
    used_features: list or None = None,
    hyper_params: dict or None = None,
    embeddngs: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None,
    **params,
) -> dict:
    """
    Обучение и добавление (в словарь ммоделей) модели WhiteBox AutoML.

    Parameters
    ----------
    data: dict
        Словарь с данными. Ключ название выборки, значение кортеж с матрицей признаков (pd.DataFrame)
        и вектором целевой переменной (pd.Series)
    config: dict
        Словарь с параметрами запуска эксперимента
    embeddngs: Optional[Dict[str, Dict[str, pd.DataFrame]]], default = None
        Словарь эмбеддингов

    Returns
    -------
    models: dict
        Словарь с моделями.

    """
    models = {}
    if config.use_lama:
        try:
            if not used_features:
                used_features = data["train"][0].columns.to_list()
            if not hyper_params:
                hyper_params = {
                    "task": config.task,
                    "loss_function": config.loss_function,
                    # for compatibility with other models, actually not used
                }

            if "eval_metric" not in hyper_params:
                hyper_params["eval_metric"] = config.eval_metric

            if "objective" not in hyper_params:
                hyper_params["objective"] = config.loss_function

            hyper_params.update(params)

            vectorization_algos = config.get("vectorization_algos", [])
            if len(vectorization_algos) > 0 and embeddngs is not None:
                for vectorization_name in vectorization_algos:
                    embeddings_df = embeddngs[vectorization_name]
                    data_cp = data.copy()
                    used_features_cp = deepcopy(used_features)
                    for sample_name, sample in data_cp.items():
                        X_sample = pd.concat(
                            [sample[0], embeddings_df[sample_name]],
                            axis=1,
                            ignore_index=False,
                        )
                        data_cp[sample_name] = (X_sample, sample[1])
                        used_features_cp = [
                            col
                            for col in data_cp["train"][0].columns
                            if col not in config.text_features
                        ]
                    models = _get_lama_model_dict(
                        models,
                        data_cp,
                        config,
                        hyper_params,
                        used_features_cp,
                        model_name=f"LAMA.{vectorization_name}",
                    )
            else:
                models = _get_lama_model_dict(
                    models, data, config, hyper_params, used_features
                )

        except AssertionError as e:
            if "Pipeline finished with 0 models" in str(e):
                _logger.warning("LAMA не смогла получить ни одной модели...")
            else:
                raise

    return models


def _get_lama_model_dict(
    models, data, config, hyper_params, used_features, model_name: str = "LAMA"
):
    lama_model = LAMA(
        estimator_params=hyper_params,
        task=config.task,
        used_features=used_features,
        metric_name=config.eval_metric,
        metric_params=config.metric_params,
        lama_time=config.lama_time,
    )
    lama_model.fit(*data["train"], *data["valid"])
    models[model_name] = lama_model
    return models