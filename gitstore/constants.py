import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIT_STORE = "gitstore"
CODE_DIR = BASE_DIR / GIT_STORE
API_DIR = CODE_DIR / "api"
PLUGINS_DIR = CODE_DIR / "plugins"
CONFIG_FILE = "config.yaml"
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"
NAME = "name"
PORT = 5000
MODIFIED_TIME = "time"
