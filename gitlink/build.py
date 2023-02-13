from gitstore.handle import GitStoreHandle
from pathlib import Path

def load(config: str) -> GitStoreHandle:
    return GitStoreHandle(Path(config))
