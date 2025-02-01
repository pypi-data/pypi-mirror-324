import time
from functools import wraps


def execution_time(func: callable):
    """
    Декоратор для замера времени выполнения функции func.

    Типичный пример использования:
    @execution_time
    def some_function(<arguments>):
        <setup>
        return res

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Func: {func.__name__}, Started at: {time.ctime()}\n")
        start_time = time.time()
        res = func(*args, **kwargs)
        exec_time = round(time.time() - start_time, 3)
        print(f"Func: {func.__name__}, Execution time: {exec_time} sec.\n")
        print(f"Func: {func.__name__}, Finished at: {time.ctime()}")
        return res

    return wrapper