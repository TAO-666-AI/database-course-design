from fastapi import APIRouter, Depends

from core.security import create_token, hash_password, verify_password
from db.connection import get_db
from dependencies.auth import current_user
from schemas.auth import LoginForm, RegisterForm
from utils.response import clean_row, err, ok

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(form: RegisterForm, db=Depends(get_db)):
    if not form.phone.isdigit():
        return err(40001, "手机号格式不正确")
    if form.password != form.confirm_password:
        return err(40002, "两次输入的密码不一致")
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username=%s OR phone=%s", (form.username, form.phone))
            if cursor.fetchone():
                return err(40901, "用户名或手机号已存在")
            cursor.execute(
                "INSERT INTO users(username, phone, password_hash) VALUES(%s,%s,%s)",
                (form.username, form.phone, hash_password(form.password)),
            )
            user_id = cursor.lastrowid
        db.commit()
        return ok({"id": user_id}, "注册成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"注册失败：{exc}")


@router.post("/login")
def login(form: LoginForm, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, phone, password_hash, role, status FROM users WHERE username=%s OR phone=%s",
                (form.account, form.account),
            )
            user = cursor.fetchone()
            if not user or not verify_password(form.password, user["password_hash"]):
                return err(40101, "账号或密码错误")
            if user["status"] != "active":
                return err(40301, "账号已被禁用")
            cursor.execute("UPDATE users SET last_login=NOW() WHERE id=%s", (user["id"],))
        db.commit()
        token = create_token(user["id"], user["username"], user["role"])
        return ok(
            {
                "token": token,
                "user": {"id": user["id"], "username": user["username"], "phone": user["phone"], "role": user["role"]},
            },
            "登录成功",
        )
    except Exception as exc:
        db.rollback()
        return err(50001, f"登录失败：{exc}")


@router.get("/me")
def me(user=Depends(current_user), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, username, phone, role, status, created_at, last_login FROM users WHERE id=%s", (user["id"],))
        row = cursor.fetchone()
    if not row:
        return err(40401, "用户不存在")
    return ok(clean_row(row))
