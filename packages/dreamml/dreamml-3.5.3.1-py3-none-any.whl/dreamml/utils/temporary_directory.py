import shutil
import os
import glob
from pathlib import Path

from dreamml.logging import get_logger

_logger = get_logger(__name__)


class TempDirectory:
    """
    Класс для управления временной папкой эксперимента
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TempDirectory, cls).__new__(cls)
        return cls._instance

    def __init__(self, path="./dml_spark_temp_dir"):
        """
        Parameters
        ----------
        directory: str
            Путь для создания временной папки
        prefix: str
            Префикс в названии временной папки
        """
        for name in glob.glob(path):
            shutil.rmtree(name)
        self.dir = Path(path)
        self.dir.mkdir()
        self.name = str(self.dir)
        _logger.info(f"Temp directory {self.name} is created.")

    def remove(self):
        """
        Удаление временной папки
        """
        shutil.rmtree(self.name, ignore_errors=False)
        _logger.info(f"Temp directory {self.name} is removed.")

    def clear(self):
        """
        Очищение временной папки
        """
        shutil.rmtree(self.name, ignore_errors=False)
        self.dir.mkdir()
        _logger.info(f"Temp directory {self.name} is cleared.")