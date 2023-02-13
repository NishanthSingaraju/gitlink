import yaml
from gitstore.utils import flatten_dictionary

class StoreConfig:
    def __init__(self, name, plugins, mappings, file_path, storage_handler = "", vars = None):
        self.name = name
        self.plugins = plugins
        self.mappings = mappings
        self.storage_handler = storage_handler
        self.file_path = file_path
        self.vars = vars
        
    @classmethod
    def from_yaml(cls, file_path):
        with open(file_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        name = data.get("name", "")
        plugins = data.get("plugins", [])
        mappings = [MappingConfig.from_dict(mapping) for mapping in data.get("mappings", [])]
        storage_handler = data.get("storage_handler", "")
        vars  = {key: flatten_dictionary(val) for key, val in data.get("vars", {}).items()}
        print(vars)
        file_path = file_path
        return cls(name, plugins, mappings, file_path, storage_handler, vars)
    
    def to_dict(self):
        return {
            "plugins": self.plugins,
            "mappings": [mapping.to_dict() for mapping in self.mappings],
            "storage_handler": self.storage_handler,
            "vars": self.vars
        }

class MappingConfig:
    def __init__(self, file_type, handler, vars=None):
        self.file_type = file_type
        self.handler = handler
        self.vars = vars or {}
        
    @classmethod
    def from_dict(cls, data):
        file_type = data.get("file_type")
        handler = data.get("handler")
        vars = data.get("vars")
        return cls(file_type, handler, vars)

    def to_dict(self):
        return {
            "file_type": self.file_type,
            "handler": self.handler,
            "vars": self.vars
        }