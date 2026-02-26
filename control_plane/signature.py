import hmac
import hashlib
from fastapi import HTTPException

SECRET = "enterprise-secret"


def verify_signature(body: bytes, signature: str):
    expected = hmac.new(
        SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
