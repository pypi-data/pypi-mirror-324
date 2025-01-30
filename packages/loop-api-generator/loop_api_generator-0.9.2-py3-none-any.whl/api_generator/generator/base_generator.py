from src.api_generator.store.store import Store
from src.api_generator.utils.filter_placeholders import filter_placeholders
from src.api_generator.utils.logger import logger_instance


class BaseGenerator:
    def __init__(self):
        self.logger = logger_instance()
        self.__store = Store()

    def append(self, id: str, text: str):
        file = self.store.get(id)
        if file is None:
            raise ValueError(f"No file found with id: {id}")
        self.store.update(id, file + text)

    def update(self, id: str, text: str):
        self.store.update(id, text)

    def clear(self, id: str):
        self.store.delete(id)

    def delete(self, id: str, text_to_delete: str):
        file = self.store.get(id)
        if file is None:
            raise ValueError(f"No file found with id: {id}")
        self.store.update(id, file.replace(text_to_delete, ""))

    def peek(self, id: str, placeholders: list[str] = []):
        self.logger.debug(filter_placeholders(self.store.get(id), placeholders))

    @property
    def store(self) -> Store:
        return self.__store
