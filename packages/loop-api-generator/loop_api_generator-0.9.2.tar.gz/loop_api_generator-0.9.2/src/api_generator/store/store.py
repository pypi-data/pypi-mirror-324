from io import BytesIO
from threading import Lock
from typing import Dict, Union

from src.api_generator.utils.generate_uuid import generate_uuid
from src.api_generator.utils.text_to_buffer import text_to_buffer


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Store(metaclass=SingletonMeta):
    def __init__(self):
        self.__storage: Dict[str, BytesIO] = {}

    def create(self, value: str):
        key = generate_uuid()
        self.__storage[key] = text_to_buffer(value)
        return key

    def get(self, key: str) -> Union[str, None]:
        return (
            self.__storage.get(key).getvalue().decode()
            if key in self.__storage
            else None
        )

    def update(self, key: str, value):
        if key not in self.__storage:
            raise ValueError(f"No file found with id: {key}")
        self.__storage[key] = text_to_buffer(value)

    def delete(self, key: str):
        del self.__storage[key]

    @property
    def storage(self) -> Dict[str, BytesIO]:
        return self.__storage
