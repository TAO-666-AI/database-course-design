from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from schemas.spot import SpotForm
from utils.response import clean_rows, err, ok

router = APIRouter(prefix="/api/admin/spots", tags=["管理员-景点管理"])


@router.get("")
def admin_spots(keyword: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = """
    SELECT id, name, category, description, open_time, location, ticket_price,
           recommended_duration, image_url, created_by, created_at, updated_at
    FROM spots
    WHERE 1=1
    """
    params = []
    if keyword:
        sql += " AND (name LIKE %s OR category LIKE %s OR location LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    sql += " ORDER BY id ASC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.post("")
def admin_create_spot(form: SpotForm, admin=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO spots(name, category, description, open_time, location, ticket_price,
                                  recommended_duration, image_url, created_by)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    form.name,
                    form.category,
                    form.description,
                    form.open_time,
                    form.location,
                    form.ticket_price,
                    form.recommended_duration,
                    form.image_url,
                    admin["id"],
                ),
            )
            item_id = cursor.lastrowid
        db.commit()
        return ok({"id": item_id}, "景点创建成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"景点创建失败：{exc}")


@router.put("/{spot_id}")
def admin_update_spot(spot_id: int, form: SpotForm, _=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE spots SET name=%s, category=%s, description=%s, open_time=%s, location=%s,
                                 ticket_price=%s, recommended_duration=%s, image_url=%s
                WHERE id=%s
                """,
                (
                    form.name,
                    form.category,
                    form.description,
                    form.open_time,
                    form.location,
                    form.ticket_price,
                    form.recommended_duration,
                    form.image_url,
                    spot_id,
                ),
            )
            if cursor.rowcount == 0:
                return err(40401, "景点不存在")
        db.commit()
        return ok(msg="景点更新成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"景点更新失败：{exc}")


@router.delete("/{spot_id}")
def admin_delete_spot(spot_id: int, _=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM spots WHERE id=%s", (spot_id,))
            if cursor.rowcount == 0:
                return err(40401, "景点不存在")
        db.commit()
        return ok(msg="景点删除成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"景点删除失败：{exc}")
