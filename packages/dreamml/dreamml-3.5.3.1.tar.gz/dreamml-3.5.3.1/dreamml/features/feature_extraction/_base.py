def drop_features(config, eval_sets):
    """
    Удаление признаков из каждого набора данных в eval_sets.
    Удаляются признаки, которые размещены в конфигурационном
    файла с ключам drop_features и target_name.

    Parameters
    ----------
    config: dict
        Конфигурационный файл.

    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]]
        Словарь с выборками, для которых требуется рассчитать статистику.
        Ключ словаря - название выборки (train / valid / ...), значение -
        кортеж с матрицей признаков (data) и вектором ответов (target).

    Returns
    -------
    eval_sets: Dict[string, Tuple[pandas.DataFrame, pandas.Series]], pandas.DataFrame
        Преобразованный eval_sets и DataFrame с признаками,  отмеченными как "drop_features"

    """

    never_used_features_cleaned = []
    dropped_features = set(
        config.get("drop_features") if config.get("drop_features") is not None else []
    )

    target_names = config.get("target_name")

    if isinstance(target_names, list):
        garbage_features = set(target_names) if target_names else set()
    else:
        garbage_features = [target_names] if target_names else []
        garbage_features = set(garbage_features)
        garbage_features |= set(config.get("multitarget", set()))

    if config.get("time_column") and not config.get("oot_data_path"):
        dropped_features.add(config.get("time_column"))
    never_used_features = config.get("never_used_features", [])

    if never_used_features:
        for feature in never_used_features:
            never_used_features_cleaned.append(feature.split("\n")[0])

    dropped_data = {}
    for sample in eval_sets:
        data, target = eval_sets[sample]
        dropped_data[sample] = data[dropped_features]
        data = data.drop(garbage_features | dropped_features, axis=1)

        extra_features_to_drop = list(
            set(data.columns) & set(never_used_features_cleaned)
        )

        if extra_features_to_drop:
            dropped_data[sample] = dropped_data[sample].join(
                data[extra_features_to_drop]
            )
            data = data.drop(extra_features_to_drop, axis=1)

        eval_sets[sample] = (data, target)

    return eval_sets, dropped_data