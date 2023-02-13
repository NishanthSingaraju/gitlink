import logging
from typing import Dict
from gitstore.constants import NAME

class Docker:
    _client = None

    @staticmethod
    def client():
        if Docker._client is None:
            from python_on_whales import docker
            Docker._client = docker
        return Docker._client

def get_containers(labels: dict, all=False):
    """Gets containers given labels."""
    return Docker.client().container.list(
        filters=_create_label_filters(labels), all=all
    )

def get_images(labels: dict):
    """Gets images given labels."""
    return Docker.client().image.list(filters=_create_label_filters(labels))


def kill_containers(labels: Dict[str, str]):
    from python_on_whales.exceptions import DockerException
    containers = get_containers(labels)
    for container in containers:
        container_labels = container.config.labels
        if NAME in container_labels:
            truss_dir = container_labels[NAME]
            logging.info(f"Killing Container: {container.id} for {truss_dir}")
    try:
        Docker.client().container.kill(containers)
    except DockerException:
        pass


def _create_label_filters(labels: Dict):
    return {
        f"label={label_key}": label_value for label_key, label_value in labels.items()
    }
