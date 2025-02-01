import numpy as np
import pandas as pd


def calculate_quantile_bins(
    data: pd.Series,
    n_bins: int = 20,
    percentile_implementation: bool = False,
    ascending: bool = False,
) -> np.ndarray:
    """
    Расчет квантильных бакетов.

    Parameters
    ----------
    data: pandas.Series
        вектор значений, для разбиения на квантили.

    n_bins: int, optional, default = 20
        количество бинов, на которые требуется разбить.

    percentile_implementation: bool
        Использовать ли версию функции из старого кода dreamml_modeling.

    ascending: bool
        В каком порядке сортировать данные перед формированием бинов.

    Returns
    -------
    data_transformed: np.ndarray
        квантильные бакеты.

    """
    if percentile_implementation:
        bins = np.linspace(0, 100, n_bins)
        perc = [np.percentile(data, x) for x in bins]
        perc = np.sort(np.unique(perc))
        return pd.cut(data, perc, labels=False, include_lowest=True)
    else:
        df = data.to_frame() if isinstance(data, pd.Series) else data
        idx = df.index.values.astype(int)
        df.rename({df.columns[0]: "data"}, axis=1, inplace=True)
        df.sort_values("data", ascending=ascending, inplace=True)
        df["bin"] = np.linspace(1, n_bins + 1, len(data), False, dtype=int)
        bins = df["bin"][idx].to_numpy()
        return bins