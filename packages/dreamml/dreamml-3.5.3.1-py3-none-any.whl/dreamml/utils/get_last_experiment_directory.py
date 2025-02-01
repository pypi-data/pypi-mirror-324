import os
from typing import Optional

from dreamml.utils.saver import BaseSaver


def get_last_experiment_dir(path_to_results: str = "../results/") -> str:
    """
    Модуль возвращает путь (типа "../results/model_with_target_run_1") последнего эксперимента по созданию моделей
    в DreamML. Последний эксперимент определяется количеством директорий в папке с результатами
    (т.е. если 35 директорий, то будет искаться эксперимент с номером 35 на конце). В случае отсутствия,
    будет выбран путь с последней датой изменения (дату создания директории получить затруднительно).

    Parameters
    ----------
    path_to_results: str
        Путь до папки с результатами экспериментов. По умолчанию "../results/" для запуска из dreamml notebooks.

    Returns
    -------
    last_experiment_dir: str
        Путь последнего эксперимента.
    """
    artifact_saver = BaseSaver(path_to_results)
    dml_dirs = artifact_saver.get_dreamml_experiment_dirs()

    last_experiment_dir = None
    last_created_time = 0
    for dml_dir in dml_dirs:
        path = os.path.join(path_to_results, dml_dir, artifact_saver._dml_version_file)

        modified_time = os.path.getmtime(path)

        if modified_time > last_created_time:
            last_created_time = modified_time
            last_experiment_dir = dml_dir

    if last_experiment_dir is None:
        raise Exception(
            "Can't determine last experiment directory. Check that the path is correct and experiments exist."
        )

    return last_experiment_dir


def get_experiment_dir_path(
    results_dir_path: str,
    experiment_dir_name: Optional[str] = None,
    use_last_experiment_directory: bool = False,
    raise_exception: bool = True,
):
    if use_last_experiment_directory:
        dir_name = get_last_experiment_dir(results_dir_path)
    else:
        if experiment_dir_name is None and raise_exception:
            raise ValueError(
                f"Требуется указать название папки с экспериментом при {use_last_experiment_directory=}"
            )
        elif not raise_exception:
            experiment_dir_name = ""
        dir_name = experiment_dir_name

    experiment_dir_path = os.path.join(results_dir_path, dir_name)

    return experiment_dir_path