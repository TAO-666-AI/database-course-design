from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from schemas.route import RouteForm
from services.route_service import build_route, save_route_spots
from utils.response import check_choice, err, ok

router = APIRouter(prefix="/api/admin/routes", tags=["管理员-路线管理"])


@router.get("")
def admin_routes(keyword: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = """
    SELECT id, name, description, difficulty, duration_hours, created_by, created_at, updated_at
    FROM routes
    WHERE 1=1
    """
    params = []
    if keyword:
        sql += " AND (name LIKE %s OR description LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like])
    sql += " ORDER BY id ASC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = [build_route(cursor, row) for row in cursor.fetchall()]
    return ok({"items": rows, "total": len(rows)})


@router.post("")
def admin_create_route(form: RouteForm, admin=Depends(current_admin), db=Depends(get_db)):
    check_choice(form.difficulty, {"easy", "medium", "hard"}, "difficulty")
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO routes(name, description, difficulty, duration_hours, created_by) VALUES(%s,%s,%s,%s,%s)",
                (form.name, form.description, form.difficulty, form.duration_hours, admin["id"]),
            )
            route_id = cursor.lastrowid
            save_route_spots(cursor, route_id, form.spot_ids)
        db.commit()
        return ok({"id": route_id}, "路线创建成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"路线创建失败：{exc}")


@router.put("/{route_id}")
def admin_update_route(route_id: int, form: RouteForm, _=Depends(current_admin), db=Depends(get_db)):
    check_choice(form.difficulty, {"easy", "medium", "hard"}, "difficulty")
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE routes SET name=%s, description=%s, difficulty=%s, duration_hours=%s WHERE id=%s",
                (form.name, form.description, form.difficulty, form.duration_hours, route_id),
            )
            if cursor.rowcount == 0:
                return err(40401, "路线不存在")
            save_route_spots(cursor, route_id, form.spot_ids)
        db.commit()
        return ok(msg="路线更新成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"路线更新失败：{exc}")


@router.delete("/{route_id}")
def admin_delete_route(route_id: int, _=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM routes WHERE id=%s", (route_id,))
            if cursor.rowcount == 0:
                return err(40401, "路线不存在")
        db.commit()
        return ok(msg="路线删除成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"路线删除失败：{exc}")
