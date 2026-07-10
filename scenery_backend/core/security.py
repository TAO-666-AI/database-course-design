import base64
import hashlib
import hmac
import json
import os
import time
from typing import Optional

from core.config import JWT_EXPIRE_HOURS, JWT_SECRET


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return base64.b64encode(salt).decode() + "$" + base64.b64encode(digest).decode()


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_b64, digest_b64 = stored.split("$", 1)
        salt = base64.b64decode(salt_b64.encode())
        expected = base64.b64decode(digest_b64.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _sign(message: str) -> str:
    digest = hmac.new(JWT_SECRET.encode("utf-8"), message.encode("ascii"), hashlib.sha256).digest()
    return _b64encode(digest)


def create_token(user_id: int, username: str, role: str) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + JWT_EXPIRE_HOURS * 3600,
    }
    head = _b64encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{head}.{body}"
    return f"{signing_input}.{_sign(signing_input)}"


def decode_token(authorization: Optional[str]) -> Optional[dict]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    try:
        head, body, signature = token.split(".")
        signing_input = f"{head}.{body}"
        if not hmac.compare_digest(_sign(signing_input), signature):
            return None
        payload = json.loads(_b64decode(body).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            return None
        return payload
    except Exception:
        return None
