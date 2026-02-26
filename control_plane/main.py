from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from .router import Router
from .database import init_db, get_metrics, get_daily_cost
from .auth import authorize
from .status import model_status
from .sla import sla_controller
from .health_score import HealthScore
from .circuit_breaker import breaker
from .model_registry import enable_model, disable_model, registry_status
from .performance import model_win_rates
from .security import check_ip
from .rate_limit import rate_limiter

app = FastAPI()
router = Router()
health_score = HealthScore()

init_db()

class RequestModel(BaseModel):
    prompt: str

@app.post("/auto")
async def auto(request: Request, req: RequestModel, x_api_key: str = Header(...)):
    check_ip(request)
    if not rate_limiter.check(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    tenant, _ = authorize(x_api_key, "azure")
    return await router.auto(req.prompt)

@app.post("/model/{model_name}")
async def call_specific(model_name: str, request: Request, req: RequestModel, x_api_key: str = Header(...)):
    check_ip(request)
    if not rate_limiter.check(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    tenant, _ = authorize(x_api_key, model_name)
    return await router.single_route(model_name, req.prompt)

@app.post("/ensemble")
async def ensemble(request: Request, req: RequestModel, x_api_key: str = Header(...)):
    check_ip(request)
    if not rate_limiter.check(x_api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    tenant, _ = authorize(x_api_key, "opus")
    return await router.ensemble(req.prompt)

@app.get("/metrics")
def metrics(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return get_metrics()

@app.get("/status")
def status(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return model_status()

@app.get("/sla")
def sla(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return sla_controller.evaluate()

@app.get("/health-score")
def health_score_endpoint(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return health_score.evaluate()

@app.get("/cost-trend")
def cost_trend(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return {
        "daily_cost": get_daily_cost(),
        "metrics": get_metrics()
    }

@app.get("/leaderboard")
def leaderboard(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return model_win_rates()

@app.get("/admin/models")
def list_models(request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    return registry_status()

@app.post("/admin/enable/{model}")
def enable(model: str, request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    enable_model(model)
    return {"model": model, "status": "enabled"}

@app.post("/admin/disable/{model}")
def disable(model: str, request: Request, x_api_key: str = Header(...)):
    check_ip(request)
    authorize(x_api_key, "azure")
    disable_model(model)
    return {"model": model, "status": "disabled"}

@app.get("/health")
def health():
    return {"status": "ok"}
