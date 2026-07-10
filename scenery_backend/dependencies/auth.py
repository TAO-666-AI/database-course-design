from typing import Optional

from fastapi import Depends, Header, HTTPException

from core.security import decode_token


def current_user(authorization: Optional[str] = Header(None)) -> dict:
    payload = decode_token(authorization)
    if not payload:
        raise HTTPException(status_code=401, detail="未登录或 token 已失效")
    return {"id": int(payload["sub"]), "username": payload.get("username"), "role": payload.get("role")}


def current_admin(user: dict = Depends(current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user
