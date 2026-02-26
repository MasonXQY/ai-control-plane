MODEL_REGISTRY = {
    "kimi": {"enabled": True},
    "opus": {"enabled": True},
    "sonnet": {"enabled": True},
    "azure": {"enabled": True}
}


def enable_model(model):
    if model in MODEL_REGISTRY:
        MODEL_REGISTRY[model]["enabled"] = True


def disable_model(model):
    if model in MODEL_REGISTRY:
        MODEL_REGISTRY[model]["enabled"] = False


def is_enabled(model):
    return MODEL_REGISTRY.get(model, {}).get("enabled", False)


def registry_status():
    return MODEL_REGISTRY
