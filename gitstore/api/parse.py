import importlib

def get_storage_handler(config):
    storage_handler_name = config['storage_handler']
    module = importlib.import_module(f"plugins.{storage_handler_name}.{storage_handler_name}")
    handler_class = getattr(module, storage_handler_name)
    return handler_class(config)

