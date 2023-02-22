import importlib
import yaml
from schema import ObjectResponse

CONFIG = 'config.yaml'

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def get_config():
    return load_config('config.yaml')


def download(oid, size):
    config = get_config()
    storage_handler = get_storage_handler(config)
    download_url, download_url_expiry = storage_handler.download(oid)
    return ObjectResponse(
            oid=oid,
            size=size,
            actions = {
                "download": {
                    "href": download_url,
                    "header": {},
                    "expires_in": download_url_expiry
                }
            }
    )

def upload(oid, size):
    config = get_config()
    storage_handler = get_storage_handler(config)
    upload_url, upload_url_expiry = storage_handler.upload(oid)
    return ObjectResponse(
            oid = oid,
            size = size,
            actions = {
                "upload": {
                    "href": upload_url,
                    "header": {},
                    "expires_in": upload_url_expiry
                }
            }
    )
    

def get_storage_handler(config: dict):
    storage_handler_name = config['storage_handler']
    config = inject_secrets(config)
    variables = {key: val for key, val in config.get("vars", {}).items()}
    module = importlib.import_module(f"{storage_handler_name}")
    handler_class = getattr(module, storage_handler_name)
    return handler_class(**variables)





def inject_secrets(config: dict):
    drain_name = config["secrets"]["drain"]
    drain = importlib.import_module(f"{drain_name}")
    drain_class = getattr(drain, drain_name)()
    for var_name, var_info in config.items():
        if var_info["type"] == "secret":
            config[var_name]["value"] = drain_class.resolve_secret(var_info["value"])
    return config


