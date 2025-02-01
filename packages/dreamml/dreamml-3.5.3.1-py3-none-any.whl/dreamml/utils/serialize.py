"""
# Модуль сериализации.
Нужен для поддержания обратной совместимости:
модели разработанные на предыдущих версиях могут быть использованы в новых версиях.

Ответственность за соблюдение сериализации лежит на разработчике.
Если вносится какое-то изменения в класс, нужно подумать, не сломается ли сериализация,
и в случае чего внести изменения в методы `serialize`, `deserialize`.

Загрузка и сохранение с помощью pickle заменяется на использование
`obj.save_pretrained(path)` и `SomeClass.from_pretrained(path)`,
также есть `AutoModel.from_pretrained(path)`, который не требует указания конкретного класса.

Если видите сообщение по типу "While loading '...' encountered '...' which is not serializable" -
значит был загружен объект с помощью from_pretrained и какой-то из атрибутов не является dreamml-сериализуемым
и был загружен просто как pickle. В этом случае, если в dreamml произойдут изменения
и либо поменяется название этого атрибута, либо этот не dreamml-сериализуемый объект поменяет название своего класса,
какие-то атрибуты, то в этом случае будет возникать ошибка загрузки объекта.

Для сериализации необходимо корректно реализовать методы `serialize`, `deserialize` (classmethod),
а также добавить класс в функцию `dreamml.utils.serialize.find_class`


## Метод serialize()

Здесь нужно создать словарь с ключами, которые будут аргументами метода __init__,
а значения словаря заполнены переменными, которые будут подаваться в метод __init__ дли инициализации.
Также опционально можно создать словарь с дополнительными параметрами,
которые в основном используются для переопределения атрибутов после инициализации.
Если какие-то объекты являются сериализуемыми, то нужно на них сделать вызов .serialize().
Выход метода:
return self._serialize(init_data=init_dict, additional_data=additional_dict)


Переопределение метода _serialize:
В случае, если вы наследуетесь от сериализуемого объекта, в котором прописан метод serialize,
можно не прописывать аргументы для инициализации и дополнительные данные заново, а переопределить метод _serialize.
у этого метода два аргумента: init_data и additional_data -- словари, которые заполнены в методе serialize.
В методе _serialize достаточно дополнить эти словари.

Выход метода:
return super()._serialize(init_data, additional_data)


## Метод deserialize(data)
Этот метод обеспечивает корректную инициализацию и заполнение атрибутов правильными значениями.
В data["init"] и data["additional"] -- это словари init_dict и additional_dict, которые были переданы в self._serialize.
Здесь нужно инициализировать объект: `instance = cls._deserialize(data)`,
предварительно заменив в data["init"] сериализуемые объекты с помощью SerializedObject(obj).deserialize(),
где obj - сериализованный объект в data["init"].
Далее можно заменить атрибуты `instance` дополнительными параметрами из data["additional"]

Выход метода:
return instance

Переопределение метода _deserialize
На вход принимает data, c ключами "init", "additional",
которые были заполнены в методах сериализации, а также "_metadata".
На выходе должен выдавать инициализированный объект, по умолчанию это cls(**data["init")

## Функция find_class
По строковому имени класса возвращает нужный класс.
Здесь важно прописать для всех сериализуемых объектов вовзращение питоновского класса по его имени.


## Сохранение обратной совместимости
- Изменение названия сериализуемого класса
Нужно в find_class возвращать класс по старому и новому имени

- Изменение названия атрибутов или аргументов
Нужно в deserialize соответственно переименовывать ключи в data["init"] и data["additional"].
Можно пользоваться сравнением dreamml.__version__ и data["_metadata"]["dml_version"]

- Изменение логики, добавление новых аргументов или атрибутов
Нужно в deserialize заполнять data["init"] и data["additional"] соответствующими параметрами, создавая объекты с нуля.

- Удаление аргументов или атрибутов
Нужно в deserialize удалять соответствующие параметры в data["init"] и data["additional"]

Во всех случаях нужно убедиться, что логика объекта будет работать

Можно использовать дополнительные параметры, сохраняющиеся вместе с объектом:

data["_metadata"]["dml_version"] - версия dreamml, в которой был сериализован объект
data["_metadata"]["python_version"] - версия python, в которой был сериализован объект
data["_metadata"]["class_name"] - название сериализованного класса
"""

import pickle
import sys
from pathlib import Path

import dreamml
from dreamml.logging import get_logger

_logger = get_logger(__name__)


def find_class(class_name):
    """
    (!) При изменении названия класса необходимо оставлять условие
    с предыдущим названием для сохранения совместимости версий Dreamml

    Импорты исполняются внутри условий, чтобы не импортить ненужные классы и избежать циклических импортов.

    Конечно, можно было бы сделать отображение имя -> путь_к_классу и через importlib импортировать,
    но тогда фунционал "Find Usages" в IDE не будет находить использование здесь.
    """

    if class_name == "BaseModel":
        from dreamml.modeling.models.estimators import BaseModel

        cls = BaseModel

    elif class_name == "XGBoostModel":
        from dreamml.modeling.models.estimators import XGBoostModel

        cls = XGBoostModel

    elif class_name == "CatBoostModel":
        from dreamml.modeling.models.estimators import CatBoostModel

        cls = CatBoostModel

    elif class_name == "LightGBMModel":
        from dreamml.modeling.models.estimators import LightGBMModel

        cls = LightGBMModel

    elif class_name == "LinearRegModel":
        from dreamml.modeling.models.estimators import LinearRegModel

        cls = LinearRegModel

    elif class_name == "AMTSModel":
        from dreamml.modeling.models.estimators import AMTSModel

        cls = AMTSModel

    elif class_name == "BertModel":
        from dreamml.modeling.models.estimators import BertModel

        cls = BertModel

    elif class_name == "BERTopicModel":
        from dreamml.modeling.models.estimators import BERTopicModel

        cls = BERTopicModel

    elif class_name == "EnsembeldaModel":
        from dreamml.modeling.models.estimators import EnsembeldaModel

        cls = EnsembeldaModel

    elif class_name == "WBAutoML":
        from dreamml.modeling.models.estimators._lama_v_1_3 import WBAutoML

        cls = WBAutoML

    elif class_name == "LDAModel":
        from dreamml.modeling.models.estimators import LDAModel

        cls = LDAModel

    elif class_name == "LAMA":
        from dreamml.modeling.models.estimators import LAMA

        cls = LAMA

    elif class_name == "LogRegModel":
        from dreamml.modeling.models.estimators import LogRegModel

        cls = LogRegModel

    elif class_name == "LogRegModel":
        from dreamml.modeling.models.estimators import LogRegModel

        cls = LogRegModel

    elif class_name == "OneVsRestClassifierWrapper":
        from dreamml.modeling.models.estimators._multioutput_wrappers import (
            OneVsRestClassifierWrapper,
        )

        cls = OneVsRestClassifierWrapper

    elif class_name == "PyBoostModel":
        from dreamml.modeling.models.estimators import PyBoostModel

        cls = PyBoostModel

    elif class_name == "CategoricalFeaturesTransformer":
        from dreamml.features.categorical import CategoricalFeaturesTransformer

        cls = CategoricalFeaturesTransformer

    elif class_name == "LogTargetTransformer":
        from dreamml.features.feature_extraction import LogTargetTransformer

        cls = LogTargetTransformer

    elif class_name == "AugmentationWrapper":
        from dreamml.features.text.augmentation import AugmentationWrapper

        cls = AugmentationWrapper

    elif class_name == "BaseVectorization":
        from dreamml.features.feature_vectorization._base import BaseVectorization

        cls = BaseVectorization

    elif class_name == "TfidfVectorization":
        from dreamml.features.feature_vectorization import TfidfVectorization

        cls = TfidfVectorization

    elif class_name == "GloveVectorization":
        from dreamml.features.feature_vectorization import GloveVectorization

        cls = GloveVectorization

    elif class_name == "BowVectorization":
        from dreamml.features.feature_vectorization import BowVectorization

        cls = BowVectorization

    elif class_name == "FastTextVectorization":
        from dreamml.features.feature_vectorization import FastTextVectorization

        cls = FastTextVectorization

    elif class_name == "Word2VecVectorization":
        from dreamml.features.feature_vectorization import Word2VecVectorization

        cls = Word2VecVectorization

    elif class_name == "TextFeaturesTransformer":
        from dreamml.features.text import TextFeaturesTransformer

        cls = TextFeaturesTransformer

    elif class_name == "DmlLabelEncoder":
        from dreamml.features.categorical._label_encoder import DmlLabelEncoder

        cls = DmlLabelEncoder

    else:
        raise TypeError(f"Couldn't find class with {class_name=}")

    return cls


def instantiate_serialized_object(data, deprecation_warning=True):
    instance = SerializedObject(data).deserialize()

    if deprecation_warning:
        _logger.warning(
            f"Loading DreamML models with `pickle.load` is deprecated. "
            f"Please use `AutoModel.from_pretrained(path)` for model loading "
            f"or directly use `{type(instance).__name__}.from_pretrained(path)`."
        )

    return instance


def no_warning_instantiate_serialized_object(data):
    return instantiate_serialized_object(data, deprecation_warning=False)


class NoDeprecationWarningUnpickler(pickle.Unpickler):
    def __init__(self, file, *args, **kwargs):
        self._filename = getattr(file, "name", None)

        if self._filename is not None:
            self._filename = Path(self._filename).name

        super().__init__(file, *args, **kwargs)

    def find_class(self, module, name):
        if (
            module == "dreamml.utils.serialize"
            and name == "instantiate_serialized_object"
        ):
            return no_warning_instantiate_serialized_object
        else:
            cls = super().find_class(module, name)

        if module.startswith("dreamml"):
            # При unpickling'е у объекта не должно быть сохраненных атрибутов из dreamml
            if not isinstance(cls, type) or not issubclass(cls, Serializable):
                _logger.warning(
                    f"While loading '{self._filename}' encountered '{name}' (from {module}) "
                    f"which is not serializable, there could be backward compatibility issues."
                )

        return cls


class SerializedObjectLoader:
    def __init__(self, data):
        self.data = data

    def __reduce__(self):
        return instantiate_serialized_object, (self.data,)


class SerializedObject:
    def __init__(self, data):
        self.data = data

    def deserialize(self):
        class_name = self.data["_metadata"]["class_name"]
        cls: Serializable = find_class(class_name)

        return cls.deserialize(self.data)


class Serializable:
    def save_pretrained(self, path):
        loader = SerializedObjectLoader(self.serialize())

        with open(path, "wb") as f:
            pickle.dump(loader, f)

    @classmethod
    def from_pretrained(cls, path):
        with open(path, "rb") as f:
            loaded = NoDeprecationWarningUnpickler(f).load()

        if isinstance(loaded, cls):
            return loaded
        elif isinstance(loaded, dict):
            return SerializedObject(loaded).deserialize()
        else:
            raise TypeError(
                f"Can't deserialize loaded data of type `{type(loaded)}` as {cls} class."
            )

    def serialize(self):
        return self._serialize()

    @classmethod
    def deserialize(cls, data):
        instance = cls._deserialize(data)

        return instance

    def _serialize(
        self,
        init_data=None,
        additional_data=None,
    ):
        if init_data is None:
            init_data = {}
        if additional_data is None:
            additional_data = {}

        metadata = {
            "dml_version": dreamml.__version__,
            "python_version": f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
            "class_name": self.__class__.__name__,
        }

        return {"init": init_data, "additional": additional_data, "_metadata": metadata}

    @classmethod
    def _deserialize(cls, data):
        init_data = data["init"]

        return cls(**init_data)
