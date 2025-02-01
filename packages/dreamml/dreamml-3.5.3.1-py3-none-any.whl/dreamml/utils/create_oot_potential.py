from typing import Optional, Dict

from dreamml.configs.config_storage import ConfigStorage
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import numpy as np
import warnings
import pandas as pd
import shap

from dreamml.modeling.metrics.metrics_mapping import metrics_mapping

forest_hyper_params = {
    "n_estimators": 500,
    "max_depth": 8,
    "n_jobs": -1,
    "random_state": 27,
}
xgb_params = {
    "objective": "binary:logistic",
    "learning_rate": 0.05,
    "max_depth": 5,
    "seed": 27,
}


def calculate_oot_metrics(
    data: dict,
    config: ConfigStorage,
    embeddngs: Optional[Dict[str, Dict[str, pd.DataFrame]]] = None,
):
    if len(config.vectorization_algos) > 0 and embeddngs:
        return {}, pd.DataFrame()

    oot_pot_dict, df_shap = {}, pd.DataFrame()
    if config.use_oot_potential and config.oot_data_path:
        oot_pot_dict = add_oot_potential(data, config)
        adv_val, df_shap = calculate_adversarial_validation(data)
        oot_pot_dict.update(adv_val)

    return oot_pot_dict, df_shap


def add_oot_potential(
    data: dict,
    config: ConfigStorage,
) -> dict:
    """
    Обучение  модели OOT Potential.

    Parameters
    ----------
    data: dict
        Словарь с данными. Ключ название выборки, значение кортеж с матрицей признаков (pd.DataFrame)
        и вектором целевой переменной (pd.Series)
    config: dict
        Словарь с параметрами запуска эксперимента

    Returns
    -------
    oot_pot_dict: dict
        Словарь с характеристиками OOT потенциала.

    """
    model = RandomForestClassifier(**forest_hyper_params)
    skf = StratifiedKFold(n_splits=3)
    X, y = data["OOT"][0], data["OOT"][1]
    dev_shape = data["train"][0].shape[0]
    oot_shape = data["OOT"][0].shape[0]
    ratio = round((dev_shape / oot_shape * 100), 2)
    X = X.fillna(0).select_dtypes(exclude=["string", "object", "datetime"])
    try:
        X = X.drop(columns=config.drop_features).to_numpy()
    except KeyError:
        X = X.to_numpy()
    lst_gini = []
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model.fit(X_train, y_train)
        y_pred = model.predict_proba(X_test)[:, 1]
        gini = round(metrics_mapping["gini"](task=config.task)(y_test, y_pred) * 100, 2)
        lst_gini.append(gini)
    oot_pot_dict = {
        "estimator": "Random Forest",
        "score": np.mean(lst_gini),
        "dev_shape": dev_shape,
        "oot_shape": oot_shape,
        "ratio dev/oot, %": ratio,
    }

    return oot_pot_dict


def calculate_adversarial_validation(data: dict):
    """
    Вычисляет Adversarial Validation и важность признаков
     Parameters
    ----------
    data: dict
        Словарь с данными. Ключ название выборки, значение кортеж с матрицей признаков (pd.DataFrame)
        и вектором целевой переменной (pd.Series)

    Returns
    -------
    adv_dict: dict
        Словарь с значением Adversarial Validation

    df: pd.DataFrame
       Матрица с отсортированными по важности признаками
    """
    combined_df = pd.DataFrame()
    for key, value in data.items():
        if key != "OOT":
            target = np.ones(value[1].shape)

        else:
            target = np.zeros(value[1].shape)
        df = value[0]
        df["target"] = target
        combined_df = combined_df.append(df)
    combined_df_shuffle = combined_df.sample(frac=1)
    X = combined_df_shuffle.drop(["target"], axis=1)
    y = combined_df_shuffle["target"]
    matrix = xgb.DMatrix(data=X, label=y)

    cross_val_results = xgb.cv(
        dtrain=matrix, params=xgb_params, nfold=3, metrics="auc", as_pandas=True
    )

    gini_adv = (2 * cross_val_results["test-auc-mean"].mean() - 1) * 100
    adv_dict = {"Adversarial Validation": gini_adv}
    model = xgb.train(dtrain=matrix, params=xgb_params)
    explainer = shap.TreeExplainer(model)
    importance_values = explainer.shap_values(X)
    columns = list(X.columns)
    importance_values = np.abs(importance_values.mean(axis=0))
    df = pd.DataFrame(columns, columns=["feature"])
    df["shap_importance"] = importance_values
    df = df.sort_values(by="shap_importance", ascending=False)

    return adv_dict, df