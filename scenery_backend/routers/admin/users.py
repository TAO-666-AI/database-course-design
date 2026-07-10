from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from schemas.user import UserRoleForm, UserStatusForm
from utils.response import check_choice, clean_rows, err, ok

router = APIRouter(prefix="/api/admin/users", tags=["管理员-用户管理"])


@router.get("")
def admin_users(keyword: str = "", role: str = "", status: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = "SELECT id, username, phone, role, status, created_at, last_login FROM users WHERE 1=1"
    params = []
    if keyword:
        sql += " AND (username LIKE %s OR phone LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like])
    if role:
        sql += " AND role=%s"
        params.append(role)
    if status:
        sql += " AND status=%s"
        params.append(status)
    sql += " ORDER BY id ASC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.put("/{user_id}/status")
def admin_user_status(user_id: int, form: UserStatusForm, admin=Depends(current_admin), db=Depends(get_db)):
    check_choice(form.status, {"active", "disabled"}, "status")
    if user_id == admin["id"] and form.status == "disabled":
        return err(40001, "不能禁用当前管理员")
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE users SET status=%s WHERE id=%s", (form.status, user_id))
            if cursor.rowcount == 0:
                return err(40401, "用户不存在")
        db.commit()
        return ok(msg="用户状态更新成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"用户状态更新失败：{exc}")


@router.put("/{user_id}/role")
def admin_user_role(user_id: int, form: UserRoleForm, admin=Depends(current_admin), db=Depends(get_db)):
    check_choice(form.role, {"tourist", "admin"}, "role")
    if user_id == admin["id"] and form.role != "admin":
        return err(40001, "不能取消当前管理员权限")
    try:
        with db.cursor() as cursor:
            cursor.execute("UPDATE users SET role=%s WHERE id=%s", (form.role, user_id))
            if cursor.rowcount == 0:
                return err(40401, "用户不存在")
        db.commit()
        return ok(msg="用户角色更新成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"用户角色更新失败：{exc}")
