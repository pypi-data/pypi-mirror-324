from collections import namedtuple

AlgoInfo = namedtuple(
    "AlgoInfo",
    [
        "algo_class",
        "algo_params",
        "cat_features",
        "text_features",
        "augmentation_params",
        "bounds_params",
        "fixed_params",
    ],
)