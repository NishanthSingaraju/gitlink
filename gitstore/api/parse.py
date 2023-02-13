import importlib
import yaml
from schema import ObjectResponse, ObjectActions,Actions


CONFIG = 'config.yaml'

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_config():
    return load_config('config.yaml')

def download(oid):
    config = get_config()
    storage_handler = get_storage_handler(config)
    download_url, download_url_expiry = storage_handler.download(oid)
    return ObjectResponse(
        oid=oid,
        actions=ObjectActions(
            download=Actions(
                expires_at=download_url_expiry,
                href=download_url
            )
        ),
        authenticated=True
    )

def upload(oid):
    config = get_config()
    storage_handler = get_storage_handler(config)
    upload_url, upload_url_expiry = storage_handler.upload(oid)
    return ObjectResponse(
        oid=oid,
        actions=ObjectActions(
            upload=Actions(
                expires_at=upload_url_expiry,
                header={"Content-Type": "application/octet-stream"},
                href=upload_url
            )
        ),
        authenticated=True
    )

def get_storage_handler(config: dict):
    storage_handler_name = config['storage_handler']
    variables = {key: flatten_dictionary(val)["value"] for key, val in config.get("vars", {}).items()}
    module = importlib.import_module(f"{storage_handler_name}")
    handler_class = getattr(module, storage_handler_name)
    return handler_class(**variables)


def flatten_dictionary(mapping):
    return {key: value for d in mapping for key, value in d.items()}

