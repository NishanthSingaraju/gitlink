from abc import ABC, abstractmethod

from pathlib import Path

class BaseSource(ABC):

    @property
    def get_secret_path(self):
        return Path(Path.home(), ".git_store", "secrets")
    
    def prepare_secret_path(self):
        path = self.get_secret_path
        path.mkdir(parents=True, exist_ok=True)
        return path

    @abstractmethod
    def resolve_secret(self, secret_name):
        pass