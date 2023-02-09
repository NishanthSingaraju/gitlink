from pathlib import Path
from typing import Dict
import requests
from requests.exceptions import ConnectionError

from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_delay,
    wait_fixed,
)

from gitstore.config import StoreConfig
from gitstore.context import DockerManager
from gitstore.constants import PORT, MODIFIED_TIME, GIT_STORE
from gitstore.docker import get_images, Docker
from gitstore.utils import get_modified_time_of_file

class GitStoreHandle:
    def __init__(self, config: Path) -> None:
        self._config_path = config
        self._config = StoreConfig.from_yaml(config)
        self._manager = DockerManager(self._config)
    
    def docker_build_setup(self, build_dir: Path = None):
        build_dir_path = Path(build_dir) if build_dir is not None else None
        self._manager.add_context(build_dir_path)
    
    def build_docker_image(self, build_dir: Path = None, tag: str = None):
        return self._build_image(
            labels=self._get_labels(),
            build_dir=build_dir,
            tag=tag,
        )

    def run_image(self,
        build_dir: Path = None,
        tag: str = None,
        local_port: int = PORT,
        detach=True):

        image = self.build_docker_image(build_dir=build_dir, tag=tag)
        labels = self._get_labels()
        envs = {}
        envs["PORT"] = local_port
        container = Docker.client().run(
                image.id,
                publish=[[local_port]],
                detach=detach,
                labels=labels,
                envs=envs,
            )
        base_url = f"http://localhost:{local_port}/"
        try:
            wait_for_server(base_url)
        except Exception as e:
            raise e
        return container

    def _build_image(
        self,
        labels: Dict[str, str],
        build_dir: Path = None,
        tag: str = None,
    ):
        image = _docker_image_from_labels(labels=labels)
        if image is not None:
            return image
        build_dir_path = Path(build_dir) if build_dir is not None else None
        build_image_result = self._manager.build_image(
            build_dir_path,
            tag,
            labels=labels,
        )
        return build_image_result
    
    def _get_labels(self) -> Dict[str, str]:
        truss_mod_time = get_modified_time_of_file(self._config_path)
        return {
            GIT_STORE: True,
            MODIFIED_TIME: truss_mod_time,
        }
    

def _docker_image_from_labels(labels: dict):
    images = get_images(labels)
    if images and isinstance(images, list):
        return images[0]

@retry(
    stop=stop_after_delay(120),
    wait=wait_fixed(2),
    retry=(
        retry_if_result(lambda response: response.status_code == 503)
        | retry_if_exception_type(ConnectionError)
    ),
)
def wait_for_server(url: str):
    print("Waiting for server")
    return requests.get(url)