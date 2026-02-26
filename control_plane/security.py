from fastapi import HTTPException, Request

ALLOWED_IPS = {
    "127.0.0.1",
    "::1"
}


def check_ip(request: Request):
    client_ip = request.client.host
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="IP not allowed")
