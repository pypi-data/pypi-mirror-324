def get_n_iterations(shape: int) -> int:
    """
    Функция для выбора количества интераций оптимизатора
    в зависимости от количества наблюдений в dev выборке.

    Parameters
        ----------
        shape: int
            Количество наблюдений в dev выборке.

        Returns
        -------
        iterations: int
            Количество итераций оптимизатора.
    """

    dict_of_shapes_and_iterations = {
        0: 300,
        10000: 200,
        25000: 150,
        50000: 100,
        75000: 50,
        100000: 20,
        200000: 10,
    }

    iterations = 0

    for key, value in dict_of_shapes_and_iterations.items():
        if shape > key:
            iterations = value

    return iterations