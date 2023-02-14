import os
from pathlib import Path
import yaml

from gitlink.constants import CONFIG_FILE, API_DIR, PLUGINS_DIR, REQUIREMENTS_PATH
from gitlink.config import StoreConfig
from gitlink.utils import copy_tree_path, copy_file_path, build_store_directory, given_or_temporary_dir
from gitlink.docker import Docker
from gitlink.template import create_dockerfile

class DockerManager:

    def __init__(self, config = StoreConfig) -> None:
        self._config = config
    
    @property
    def default_tag(self):
        return f"{self._config.name}:latest"

    def build_image(self, build_dir: Path = None, tag: str = None, labels: dict = None):
        with given_or_temporary_dir(build_dir) as build_dir_path:
            self.add_context(build_dir_path)
            return Docker.client().build(
                    str(build_dir_path),
                    labels=labels if labels else {},
                    tags=tag or self.default_tag,
            )

    def add_context(self, target_directory_path: Path = None):
        if target_directory_path is None:
            target_directory_path = build_store_directory()

        with (target_directory_path / CONFIG_FILE).open("w") as config_file:
            yaml.dump(self._config.to_dict(), config_file)

        api_file_path = target_directory_path
        api_template_path = API_DIR
        copy_tree_path(api_template_path, api_file_path)
        copy_file_path(REQUIREMENTS_PATH, target_directory_path / "requirements.txt")
        self._copy_over_plugins(target_directory_path)
        self._copy_over_file_vars(target_directory_path)
        copy_file_path(self._config.file_path, target_directory_path / "config.yaml")
        create_dockerfile(self._config.to_dict(), target_directory_path)
        return target_directory_path


    def _copy_over_plugins(self, target_directory_path):
        for plugin in self._config.plugins:
            plugin_path = Path(PLUGINS_DIR) / plugin / (plugin + ".py")
            if plugin_path.exists():
                target_path = target_directory_path / (plugin + ".py")
                copy_file_path(str(plugin_path), str(target_path))
                
    
    def _copy_over_file_vars(self, target_directory_path):
        files = [value["value"] for key, value in self._config.vars.items() if value["type"] == "filepath"]
        for file in files:
            target_file_path = target_directory_path / os.path.basename(file)
            copy_file_path(str(file), str(target_file_path))