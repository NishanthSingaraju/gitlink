from abc import ABC, abstractmethod
from pathlib import Path

class BaseDrain(ABC):

    @staticmethod
    def _secrets_mount_dir_path():
        return Path("/secret")

    @abstractmethod
    def resolve_secret(self, secret_name):
        pass