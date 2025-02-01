from hyperopt import hp


hyperopt_grid = {
    "xgboost": {
        "eta": hp.quniform("eta", 0.025, 0.5, 0.025),
        "max_depth": hp.quniform("max_depth", 1, 8, 1),
        "min_child_weight": hp.quniform("min_child_weight", 1, 2500, 10),
        "colsample_bytree": hp.quniform("colsample_bytree", 0.5, 1, 0.05),
        "subsample": hp.quniform("subsample", 0.5, 1, 0.05),
        "reg_lambda": hp.quniform("reg_lambda", 0, 100, 1),
        "reg_alpha": hp.quniform("reg_alpha", 0, 100, 1),
        "gamma": hp.quniform("gamma", 0.5, 1, 0.05),
    },
    "catboost": {
        "max_depth": hp.quniform("max_depth", 3, 7, 1),
        "l2_leaf_reg": hp.quniform("l2_leaf_reg", 1, 100, 1),
        "colsample_bylevel": hp.quniform("colsample_bylevel", 0.6, 0.9, 0.1),
    },
    "lightgbm": {
        "max_depth": hp.quniform("max_depth", 3, 10, 1),
        "num_leaves": hp.quniform("num_leaves", 25, 55, 1),
        "min_split_gain": hp.quniform("min_split_gain", 0.01, 10, 0.01),
        "reg_lambda": hp.quniform("reg_lambda", 0.1, 100, 0.1),
        "reg_alpha": hp.quniform("reg_alpha", 0.1, 100, 0.1),
    },
}