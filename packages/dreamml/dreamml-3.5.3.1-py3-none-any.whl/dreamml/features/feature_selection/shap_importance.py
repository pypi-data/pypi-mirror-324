import shap
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

from dreamml.logging import get_logger
from dreamml.modeling.models.estimators import PyBoostModel

_logger = get_logger(__name__)


def _calculate_shap_values(estimator, data: pd.DataFrame, **params) -> list:
    """
    Вычисление Shap-values для объекта экземпляра модели.

    Parameters
    ----------
    estimator: sklearn.estimator
        Экземпляр модели, которая поддерживает API sklearn.
        Ожидается, что модель обучена, т.е. был вызван метод fit ранее

    data: pandas.core.frame.DataFrame
        Матрица признаков для вычисления Shap-values.

    params: Dict
        Словарь с параметрами для финкции подсчета важности признаков.

    Returns
    -------
    shap_values: numpy.array
        Матрица Shap-values.

    """
    if isinstance(estimator, PyBoostModel):
        explainer = shap.PermutationExplainer(
            estimator, masker=shap.maskers._tabular.Tabular(data)
        )
    else:
        explainer = shap.TreeExplainer(estimator.estimator)

    # Параметры бустера не сохраняются в pickle, поэтому при загрузки там пустой список
    if estimator.model_name == "LightGBM":
        estimator.estimator._Booster.params = estimator.params

    try:
        if isinstance(explainer, shap.PermutationExplainer):
            shap_values = explainer.shap_values(
                X=data[estimator.used_features], npermutations=5, **params
            )
        else:
            shap_values = explainer.shap_values(
                X=data[estimator.used_features], **params
            )
    except ValueError:
        data = xgb.DMatrix(data[estimator.used_features])
        shap_values = explainer.shap_values(X=data)
    except Exception as e:
        _logger.exception(
            f"Unexpected error while getting shap values: {e}. Trying to set 'check_additivity' parameter to `False`."
        )
        if isinstance(explainer, shap.PermutationExplainer):
            shap_values = explainer.shap_values(
                X=data[estimator.used_features], npermutations=5, **params
            )
        else:
            shap_values = explainer.shap_values(
                X=data[estimator.used_features], check_additivity=False, **params
            )

    if isinstance(shap_values, list):
        return shap_values[0]
    return shap_values


def calculate_shap_feature_importance(
    estimator, data: pd.DataFrame, fraction_sample: float = 1.0, random_seed: int = 27
) -> pd.DataFrame:
    """
    Вычисление и сортировка важности признаков на
    основе Shap-values.
    Parameters
    ----------
    estimator: sklearn.estimator
        Экземпляр модели, которая поддерживает API sklearn.
        Ожидается, что модель обучена, т.е. был вызван метод fit ранее

    data: pandas.core.frame.DataFrame
        Матрица признаков для вычисления Shap-values.

    fraction_sample: float, optional, default = 1.0,
        Доля наблюдений от data для оценки важности признаков.

    random_seed: int
        Random seed.

    Returns
    -------
    importance: pandas.core.frame.DataFrame
        Матрица с отсортированными по важности признаками.

    """
    np.random.seed(random_seed)
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            f"data must be pandas.core.DataFrame, " f"but data is {type(data)}"
        )

    if fraction_sample < 0 or fraction_sample > 1:
        raise ValueError(
            f"fraction_sample must be in range [0, 1], "
            f"but fraction_sample is {fraction_sample}"
        )
    elif 0 < fraction_sample < 1:
        x, _ = train_test_split(
            data, train_size=fraction_sample, random_state=random_seed
        )
    else:  # fraction_sample = 0 or fraction_sample = 1
        x = data

    shap_values = _calculate_shap_values(estimator=estimator, data=x)
    importance = pd.DataFrame(
        {
            "feature": estimator.used_features,
            "importance": np.abs(shap_values.mean(axis=0)),
        }
    )
    importance = importance.sort_values(by="importance", ascending=False)
    importance = importance.reset_index(drop=True)

    return importance