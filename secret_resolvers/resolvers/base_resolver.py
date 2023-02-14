from abc import ABC, abstractmethod

class Resolver(ABC):
    @abstractmethod
    def resolve_secret(self, secret_name):
        pass