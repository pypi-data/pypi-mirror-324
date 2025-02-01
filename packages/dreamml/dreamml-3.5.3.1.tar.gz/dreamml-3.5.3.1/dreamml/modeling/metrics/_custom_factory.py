import numpy as np


def _lightgbm_custom_metric_factory(self, y_true, y_pred):
    result = self._score_function(y_true, y_pred)

    return self.name, result, self.maximize


def _lightgbm_custom_objective_factory(self, y_true, y_pred):
    grad = self._get_gradient(y_true, y_pred)
    hess = self._get_hessian(y_true, y_pred)

    return grad, hess


def _pyboost_custom_metric_factory(self, y_true, y_pred):
    result = self._score_function(y_true, y_pred)

    return self.name, result, self.maximize


def _pyboost_custom_objective_factory(self, y_true, y_pred):
    grad, hess = self._get_gradient(
        y_true, y_pred
    )  # grad and hess is computed in pyboost get_grad_hess method together
    return grad, hess


def _xgboost_custom_metric_factory(self, y_true, y_pred):
    result = self._score_function(y_true, y_pred)

    return result


def _xgboost_custom_objective_factory(self, y_true, y_pred):
    grad = self._get_gradient(y_true, y_pred)
    hess = self._get_hessian(y_true, y_pred)

    return grad, hess


# https://github.com/catboost/catboost/blob/master/catboost/tutorials/custom_loss/custom_loss_and_metric_tutorial.ipynb
class _CatBoostCustomMetricFactory:
    def __init__(self, *args, _custom_metric_parent=None, **kwargs):
        self._custom_metric_parent = _custom_metric_parent

    def is_max_optimal(self):
        return self._custom_metric_parent.maximize

    def evaluate(self, approxes, target, weight):
        assert len(target) == len(approxes[0])
        if self._custom_metric_parent._task == "binary":
            approxes = approxes[0]
        else:
            approxes = np.array(approxes).T
        # weight parameter can be None.
        # Returns pair (error, weights sum)
        result = self._custom_metric_parent._score_function(target, approxes)
        return result, 0

    def get_final_error(self, error, weight):
        return error


class _CatboostCustomObjective(object):

    def __init__(self, outer_parent):
        self.outer_parent = outer_parent

    def calc_ders_range(self, approxes, targets, weights):
        assert len(approxes) == len(targets)
        if weights is not None:
            assert len(weights) == len(approxes)

        der1 = -self.outer_parent._get_gradient(
            targets, approxes
        )  # Минус перед производной стоит для того, чтобы привести к формату Xgboost и Lightgbm
        der2 = -self.outer_parent._get_hessian(targets, approxes)

        if weights is not None:
            der1 *= weights
            der2 *= weights

        result = []
        for index in range(len(targets)):
            result.append((der1[index], der2[index]))

        return result


class _CatboostCustomMultiObjective(object):

    def __init__(self, outer_parent):
        self.outer_parent = outer_parent

    def calc_ders_multi(self, approxes, targets, weight):
        der1 = -self.outer_parent._get_gradient(targets, approxes)
        der2 = -self.outer_parent._get_hessian(targets, approxes)

        return der1, der2