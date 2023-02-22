from abc import ABC, abstractmethod
from pathlib import Path

class SecretDrain(ABC):

    @staticmethod
    def _secrets_mount_dir_path():
        return Path("/secret")

    @abstractmethod
    def resolve_secret(self, secret_name):
        secret_path = SecretDrain._secrets_mount_dir_path() / secret_name
        if secret_path.exists() and secret_path.is_file():
            with secret_path.open() as secret_file:
                secret_value = secret_file.read()
        return secret_value