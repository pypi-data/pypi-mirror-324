from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def generate_get(self):
        pass

    @abstractmethod
    def generate_post(self):
        pass

    @abstractmethod
    def generate_put(self):
        pass

    @abstractmethod
    def generate_patch(self):
        pass

    @abstractmethod
    def generate_delete(self):
        pass

    @abstractmethod
    def finalize(self):
        pass
