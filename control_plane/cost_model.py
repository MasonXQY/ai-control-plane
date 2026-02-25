MODEL_COST = {
    "kimi": 0.001,
    "sonnet": 0.003,
    "opus": 0.01
}


def estimate_cost(model, token_estimate):
    return MODEL_COST.get(model, 0) * token_estimate
