import importlib

DRAIN_MAPPING = {
    "mount": "MountDrain"
}

def inject_secrets(config: dict):
    drain_name = DRAIN_MAPPING[config["secrets"]["drain"]]
    drain = importlib.import_module(f"{drain_name}")
    drain_class = getattr(drain, drain_name)()
    for var_name, var_info in config.items():
        if var_info["type"] == "secret":
            config[var_name]["value"] = drain_class.resolve_secret(var_info["value"])
    return config
