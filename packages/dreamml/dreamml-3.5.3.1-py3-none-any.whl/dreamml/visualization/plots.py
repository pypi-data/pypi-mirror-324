"""
Модуль с реализацией функций для отрисовки графиков.

Доступные сущности:
- plot_roc_curve: построение ROC-кривой.
- plot_precision_recall_curve: построение PR-AUC кривой.
- plot_mean_pred_and_target: построение кривой среднего прогноза в бакете
  и среднего ответа в бакете.
- plot_binary_graph: построение всех кривой на едином полотне.
"""

from collections import defaultdict

import numpy as np
import pandas as pd
from typing import Dict, List

from nltk import word_tokenize
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import average_precision_score, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns

from dreamml.logging import get_logger
from dreamml.modeling.metrics.metrics_mapping import metrics_mapping
from dreamml.modeling.metrics.utils import calculate_quantile_bins

_logger = get_logger(__name__)


def plot_roc_curve(y_true, y_pred):
    """
    Построение графика ROC-кривой.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """
    plt.title("ROC-Curve", size=13)
    fpr, tpr, _ = roc_curve(y_true, y_pred)
    gini = metrics_mapping["gini"](task="binary")(y_true, y_pred)
    label = "GINI: {:.4f}".format(gini)

    plt.plot(fpr, tpr, linewidth=3, label=label.format(gini), color="#534275")
    plt.plot([0, 1], [0, 1], linestyle="--", color="black", alpha=0.25)
    plt.legend(loc="best", fontsize=13)
    plt.xlabel("False Positive Rate (Sensitivity)", size=13)
    plt.ylabel("True Positive Rate (1 - Specificity)", size=13)
    plt.xlim(0, 1)
    plt.ylim(0, 1)


def plot_precision_recall_curve(y_true, y_pred):
    """
    Построение графика для Precision-Recall кривой.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.
    """
    plt.title("Precision-Recall Curve", size=13)
    precision, recall, _ = precision_recall_curve(y_true, y_pred)
    pr_auc = average_precision_score(y_true, y_pred)

    plt.plot(
        recall,
        precision,
        color="#534275",
        linewidth=3,
        label="PR-AUC:{:.4f}".format(pr_auc),
    )
    plt.axhline(np.mean(y_true), color="black", alpha=0.5, linestyle="--")
    plt.legend(loc="best", fontsize=13)
    plt.ylabel("precision", size=13)
    plt.xlabel("recall", size=13)
    plt.xlim(0, 1)
    plt.ylim(0, 1)


def plot_mean_prediction_in_bin(y_true, y_pred, n_bins: int = 20):
    """
    Построение графика зависимости среднего прогноза и среднего
    значения целевой переменной в бине.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    n_bins: integer, optional, default = 20
        Количество квантильных бинов.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """
    y_pred_mean, y_true_mean, bins = mean_by_bin(n_bins, y_pred, y_true)
    plt.plot(y_pred_mean.values, linewidth=3, color="#534275", label="y-pred")
    plt.plot(y_true_mean.values, linewidth=3, color="#427553", label="y-true")
    plt.xticks(ticks=range(n_bins), labels=range(0, n_bins, 1))
    plt.xlim(0, np.max(bins[bins <= n_bins]))
    plt.xlabel("bin_number", size=13)

    if y_true.nunique() <= 2:
        plt.ylabel("eventrate", size=13)
    else:
        plt.ylabel("mean-target", size=13)

        y_true_bins = pd.Series(y_true).groupby(bins)
        y_true_25p = y_true_bins.apply(lambda x: np.percentile(x, 25))
        y_true_50p = y_true_bins.apply(lambda x: np.percentile(x, 50))
        y_true_75p = y_true_bins.apply(lambda x: np.percentile(x, 75))
        plt.plot(
            y_true_25p.values,
            label="real 25-percentile",
            color="orange",
            linestyle="--",
            alpha=0.5,
        )
        plt.plot(
            y_true_50p.values,
            label="real 50-percentile",
            color="orange",
            linewidth=2,
            alpha=0.5,
        )
        plt.plot(
            y_true_75p.values,
            label="real 75-percentile",
            color="orange",
            linestyle="--",
            alpha=0.5,
        )

    plt.legend(loc="best", fontsize=13)


def plot_mean_pred_and_target(y_true, y_pred, n_bins: int = 20):
    """
    Построение графика зависимости среднего прогноза в
    бакете против среднего значения целевой метки в бакете.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    n_bins: integer, optional, default = 20
        Количество квантильных бинов.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """
    y_pred_mean, y_true_mean, _ = mean_by_bin(n_bins, y_pred, y_true)
    plt.plot(y_pred_mean.values, y_true_mean.values, linewidth=3, color="#534275")
    plt.plot(
        [0, max(y_pred_mean.values)],
        [0, max(y_true_mean.values)],
        color="black",
        alpha=0.5,
        linestyle="--",
    )
    plt.xlim(min(y_pred_mean.values), max(y_pred_mean.values))
    plt.ylim(min(y_pred_mean.values), max(y_true_mean.values))
    plt.xlabel("mean-prediction", size=13)

    if y_true.nunique() <= 2:
        plt.ylabel("eventrate", size=13)
    else:
        plt.ylabel("mean-target", size=13)


def mean_by_bin(n_bins, y_pred, y_true):
    df = pd.DataFrame()
    df["y_true"] = np.array(y_true)
    df["y_pred"] = np.array(y_pred)
    df.sort_values("y_pred", ascending=True, inplace=True)
    bins = calculate_quantile_bins(df["y_pred"], n_bins=n_bins)
    y_pred_mean = pd.Series(df["y_pred"]).groupby(bins).mean()
    y_true_mean = pd.Series(df["y_true"]).groupby(bins).mean()
    del df
    return y_pred_mean, y_true_mean, bins


def plot_scatter(y_true, y_pred):
    """
    Построение scatter-plot y_true vs y_pred.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """
    y_true = np.array(y_true.tolist())
    y_pred = np.array(y_pred.tolist())
    n_points = np.max([10000, 0.1 * len(y_pred)])
    n_points = np.min([n_points, len(y_pred)])

    indexes = np.random.randint(0, len(y_true), int(n_points))
    y_true_, y_pred_ = y_true[indexes], y_pred[indexes]

    plt.scatter(y_true_, y_pred_, alpha=0.25, color="#534275")
    plt.plot(
        [y_true_.min(), y_true_.max()],
        [y_true_.min(), y_true_.max()],
        color="orange",
        linestyle="--",
        linewidth=3,
    )
    plt.xlim(np.percentile(y_pred, 1), np.percentile(y_pred, 99))
    plt.ylim(np.percentile(y_pred, 1), np.percentile(y_pred, 99))
    plt.ylabel("y_real", size=14)
    plt.xlabel("y_true", size=14)


def plot_binary_graph(y_true, y_pred, save_path: str, plot_dim=(18, 4)):
    """
    Построение графиков для бинарной классификации.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    save_path: string
        Имя файла для сохранения графика.

    plot_dum: Tuple[int, int], optional, default = (16, 4)
        Размер графиков.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """

    mask = ~np.isnan(y_true)
    y_true, y_pred = y_true[mask], y_pred[mask]

    fig = plt.figure(figsize=plot_dim)
    plt.subplot(141)
    plot_roc_curve(y_true, y_pred)

    plt.subplot(142)
    plot_precision_recall_curve(y_true, y_pred)

    plt.subplot(143)
    try:
        plot_mean_prediction_in_bin(y_true, y_pred)
    except (ValueError, TypeError) as e:
        _logger.exception(f"Error occured during plot_mean_prediction_in_bin: {e}")

    plt.subplot(144)
    try:
        plot_mean_pred_and_target(y_true, y_pred)
    except (ValueError, TypeError) as e:
        _logger.exception(f"Error occured during plot_mean_pred_and_target: {e}")

    plt.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close()


def plot_model_quality_per_segment_graph(target_per_group: Dict, save_path: str):
    fig, axes = plt.subplots(
        len(target_per_group),
        1,
        figsize=(4, 3 * len(target_per_group)),
        squeeze=False,
    )

    for idx, (group, target_per_sample) in enumerate(target_per_group.items()):
        for sample_name, targets in target_per_sample.items():
            y_true, y_pred = targets

            if len(y_true) == 0:
                continue

            fpr, tpr, _ = roc_curve(y_true, y_pred)
            metric = metrics_mapping["gini"](task="binary")
            score = metric(y_true, y_pred) * 100
            label = f"{sample_name}, Gini: {score:.1f}%"

            axes[idx][0].plot(fpr, tpr, linewidth=3, label=label)

        axes[idx][0].legend(loc="best", fontsize=8)

        axes[idx][0].set_xlabel("False Positive Rate (Sensitivity)", size=7)
        axes[idx][0].set_ylabel("True Positive Rate (1 - Specificity)", size=7)

        axes[idx][0].set_xlim(0, 1)
        axes[idx][0].set_ylim(0, 1)

        axes[idx][0].plot([0, 1], [0, 1], linestyle="--", color="red", alpha=0.25)
        axes[idx][0].set_title(f"Segment {group}", size=13)
        plt.subplots_adjust(hspace=0.3)

    fig.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close()


def plot_quality_dynamics_per_segment_graph(
    time_per_group: Dict, target_per_group: Dict, save_path: str
):
    fig, axes = plt.subplots(
        len(target_per_group),
        1,
        figsize=(6, 4 * len(target_per_group)),
        squeeze=False,
    )

    for idx, (group, target_per_sample) in enumerate(target_per_group.items()):
        all_target_sum_per_time = defaultdict(dict)
        all_data_len_per_time = defaultdict(dict)

        for sample_name, targets in target_per_sample.items():
            y_true, y_pred = targets
            time_array = time_per_group[group][sample_name]

            if len(y_true) == 0:
                continue

            metric = metrics_mapping["gini"](task="binary")

            unique_times = sorted(time_array.unique())
            time_scores = []
            for time in unique_times:
                mask = time_array == time

                y_true_per_time = y_true[mask]
                if y_true_per_time.nunique() == 1:
                    _logger.warning(
                        f"Только один класс представлен в целевой переменной на времени {time}. "
                        f"Не удается посчитать метрику GINI для этого случая, считаем метрику равной 0."
                    )
                    time_score = 0.0
                else:
                    time_score = metric(y_true_per_time, y_pred[mask]) * 100
                time_scores.append(time_score)

                all_target_sum_per_time[time][sample_name] = y_true[mask].sum()
                all_data_len_per_time[time][sample_name] = len(y_true[mask])

            label = f"GINI_{sample_name}"

            axes[idx][0].plot(
                unique_times, time_scores, linewidth=3, label=label, marker="o"
            )

        times = sorted(list(all_target_sum_per_time.keys()))
        event_rates = []
        for time in times:
            all_samples_target_sum = sum(all_target_sum_per_time[time].values())
            all_samples_data_len = sum(all_data_len_per_time[time].values())

            event_rates.append(all_samples_target_sum / all_samples_data_len * 100)

        axes[idx][0].plot(
            times, event_rates, linewidth=3, label="Event_rate", marker="o"
        )

        axes[idx][0].legend(loc="best", fontsize=8)
        axes[idx][0].set_title(f"Segment {group}", size=13)
        axes[idx][0].tick_params(axis="x", labelrotation=45)
        axes[idx][0].grid(alpha=0.3)

    plt.subplots_adjust(hspace=0.4)
    fig.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close()


def plot_data_decile_statistics_graph(data, save_path: str):
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))

    ax.bar(np.arange(len(data)), data["Кол-во наблюдений"], label="Кол-во наблюдений")

    handles1, labels1 = ax.get_legend_handles_labels()

    ax2 = ax.twinx()
    ax2.plot(
        np.arange(len(data)),
        data["Event-rate (факт.)"],
        label="Event-rate (факт.)",
        color="tab:orange",
        marker="o",
    )

    ax2.set_ylim(0, 100)
    ax2.set_yticks(np.linspace(0, 100, 11))
    vals = ax2.get_yticks()
    ax2.set_yticklabels([f"{int(x)}%" for x in vals])

    handles2, labels2 = ax2.get_legend_handles_labels()

    ax.legend(handles1 + handles2, labels1 + labels2)

    fig.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close()


def plot_regression_graph(y_true, y_pred, name: str, plot_dim=(10, 4)):
    """
    Построение графиков для задачи регрессии.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, ]
        Вектор целевой переменной.

    y_pred: array-like, shape = [n_samples, ]
        Вектор прогнозов.

    name: string
        Имя файла для сохранения графика.

    plot_dum: Tuple[int, int], optional, default = (16, 4)
        Размер графиков.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.

    """
    fig = plt.figure(figsize=plot_dim)
    plt.subplot(131)
    plot_scatter(y_true, y_pred)

    plt.subplot(132)
    try:
        plot_mean_prediction_in_bin(y_true, y_pred)
    except (ValueError, TypeError) as e:
        _logger.exception(f"Error occured during plot_mean_prediction_in_bin: {e}")

    plt.subplot(133)
    try:
        plot_mean_pred_and_target(y_true, y_pred)
    except (ValueError, TypeError) as e:
        _logger.exception(f"Error occured during plot_mean_prediction_in_bin: {e}")

    plt.savefig(f"{name}.png")
    plt.close()


def plot_STL(segment_name: str, stl_dict: Dict, name: str, plot_dim=(12, 8)):
    """
    Построение графика для STL разложения [y, trend, seasonal, residual]

    Paramentrs
    ----------
    ts: array-like, shape = [n_samples, ]
        index - datetime, value - target.

    stl_dict: Dict,
        Словарь с компонентами разложения.

    name: string
        Имя файла для сохранения графика.

    plot_dum: Tuple[int, int], optional, default = (16, 4)
        Размер графикa.
    """

    fig = plt.figure(figsize=plot_dim)
    plt.title(f"Segment: {segment_name}")

    ax_1 = fig.add_subplot(4, 1, 1)
    ax_1.plot(stl_dict["timeseries"], stl_dict["target"], label="target", color="blue")
    ax_1.legend(loc="best")
    ax_1.grid(True)

    ax_2 = fig.add_subplot(4, 1, 2)
    ax_2.plot(stl_dict["timeseries"], stl_dict["trend"], label="trend", color="orange")
    ax_2.legend(loc="best")
    ax_2.grid(True)

    ax_3 = fig.add_subplot(4, 1, 3)
    ax_3.plot(
        stl_dict["timeseries"], stl_dict["seasonal"], label="seasonal", color="green"
    )
    ax_3.legend(loc="best")
    ax_3.grid(True)

    ax_4 = fig.add_subplot(4, 1, 4)
    ax_4.plot(stl_dict["timeseries"], stl_dict["resid"], label="resid", color="red")
    ax_4.legend(loc="best")
    ax_4.grid(True)

    plt.savefig(f"{name}.png")
    plt.close()


def plot_multi_graph(y_true, y_pred_proba, save_path, classes, plot_dim=(14, 4)):
    """
    Построение графиков для мультиклассовой классификации.

    Parameters
    ----------
    y_true: array-like, shape = [n_samples, n_classes]
        Вектор истинных меток для каждого класса.

    y_pred_proba: array-like, shape = [n_samples, n_classes]
        Матрица прогнозов вероятностей для каждого класса.

    save_path: string
        Имя файла для сохранения графика.

    plot_dim: Tuple[int, int], optional, default=(18, 4)
        Размер графика.

    Returns
    -------
    lines:
        Список `.Line2D` объектов, графически представляющие данные.
    """
    fig, axes = plt.subplots(1, 3, figsize=plot_dim, dpi=100)

    # ROC curve
    ax = axes[0]
    ax.set_title("ROC Curve", size=13)
    for i, class_name in enumerate(classes):
        y_true_class = y_true[:, i]
        y_pred_class = y_pred_proba[:, i]

        y_true_mask = np.isnan(y_true_class)
        y_true_class = y_true_class[~y_true_mask]
        y_pred_class = y_pred_class[~y_true_mask]

        fpr, tpr, _ = roc_curve(y_true_class, y_pred_class)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, label=f"Class {class_name} (AUC = {roc_auc:.3f})")

    ax.plot([0, 1], [0, 1], linestyle="--", color="black", alpha=0.25)
    ax.legend(loc="best", fontsize=5)
    ax.set_xlabel("False Positive Rate", size=10)
    ax.set_ylabel("True Positive Rate", size=10)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    # Precision-Recall curve
    ax = axes[1]
    ax.set_title("Precision-Recall Curve", size=13)
    for i, class_name in enumerate(classes):
        y_true_class = y_true[:, i]
        y_pred_class = y_pred_proba[:, i]

        y_true_mask = np.isnan(y_true_class)
        y_true_class = y_true_class[~y_true_mask]
        y_pred_class = y_pred_class[~y_true_mask]

        precision, recall, _ = precision_recall_curve(y_true_class, y_pred_class)
        pr_auc = average_precision_score(y_true_class, y_pred_class)
        ax.plot(recall, precision, label=f"Class {class_name} (AP = {pr_auc:.3f})")

    ax.legend(loc="best", fontsize=5)
    ax.set_xlabel("Recall", size=10)
    ax.set_ylabel("Precision", size=10)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    # Distribution of predicted probabilities
    ax = axes[2]
    ax.set_title("Predicted Probabilities Distribution", size=13)
    for i, class_name in enumerate(classes):
        y_true_class = y_true[:, i]
        y_pred_class = y_pred_proba[:, i]

        y_true_mask = np.isnan(y_true_class)
        y_true_class = y_true_class[~y_true_mask]
        y_pred_class = y_pred_class[~y_true_mask]

        ax.hist(
            y_pred_class, bins=20, alpha=0.5, label=f"Class {class_name}", density=True
        )
    ax.legend(loc="best", fontsize=5)
    ax.set_xlabel("Predicted Probability", size=10)
    ax.set_ylabel("Density", size=10)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0.1)


def plot_token_length_distribution_for_text_features(
    sample_name: str,
    text_feature: str,
    x_sample: pd.DataFrame,
    save_path: str,
    n_bins=50,
):
    """
    Построение гистограммы длины токенов.
    """
    token_length_series = x_sample[text_feature].apply(
        lambda text: len(word_tokenize(str(text)))
    )

    len_token_quantiles_dict = {}
    for quantile in [0.25, 0.5, 0.75, 0.9, 0.95, 0.97, 0.99]:
        q_len = token_length_series.quantile(quantile)
        len_token_quantiles_dict[str(quantile)] = q_len

    plt.figure(figsize=(7, 4))
    sns.histplot(token_length_series, bins=n_bins, kde=True, color="lightgreen")

    colors = ["green", "blue", "purple", "orange", "red", "brown", "magenta"]
    for i, (quantile, value) in enumerate(len_token_quantiles_dict.items()):
        plt.axvline(
            x=value,
            color=colors[i],
            linestyle="--",
            linewidth=1,
            label=f"{quantile} quantile={int(value)}",
        )

    plt.title(
        f"Distibution of Token Length | Feature: {text_feature} | Sample: {sample_name}",
        fontsize=10,
    )
    plt.xlabel("Token Length", fontsize=8)
    plt.ylabel("Frequency", fontsize=8)
    plt.legend(title="Quantile | Length", fontsize=6, title_fontsize=6)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0.1)
    plt.close()