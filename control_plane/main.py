from fastapi import FastAPI
from pydantic import BaseModel
from .router import Router
from .observability import observability

app = FastAPI()
router = Router()

class Request(BaseModel):
    prompt: str

@app.post("/auto")
async def auto(req: Request):
    return await router.auto(req.prompt)

@app.post("/ensemble")
async def ensemble(req: Request):
    return await router.ensemble(req.prompt)

@app.get("/metrics")
def metrics():
    return observability.metrics()

@app.get("/health")
def health():
    return {"status": "ok"}
