import dataclasses


# TODO добавить хранение названия метрики, для которой считался cv_score,
#  чтобы можно было выводить в отчёт gini и разные метрики для регерссии.
@dataclasses.dataclass
class CVScores:
    """
    Класс для хранения значений метрики cv score основных моделей и моделей other models
    """

    stage_models: dict = dataclasses.field(default_factory=dict)
    other_models: dict = dataclasses.field(default_factory=dict)

    @property
    def is_full(self):
        """
        Был ли заполенен словарь с моделями, по сути cv или нет
        Returns
        -------
        flag: bool
            Есть ли cv score для моделей или нет
        """
        return self.stage_models or self.other_models