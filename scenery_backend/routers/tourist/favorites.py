import pymysql
from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_user
from utils.response import clean_rows, err, ok

router = APIRouter(prefix="/api/favorites", tags=["收藏"])


@router.get("")
def my_favorites(user=Depends(current_user), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT f.id AS favorite_id, f.created_at AS favorited_at,
                   s.id, s.name, s.category, s.description, s.location, s.image_url
            FROM favorites f
            JOIN spots s ON f.spot_id=s.id
            WHERE f.user_id=%s
            ORDER BY f.created_at DESC
            """,
            (user["id"],),
        )
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.post("/{spot_id}")
def add_favorite(spot_id: int, user=Depends(current_user), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM spots WHERE id=%s", (spot_id,))
            if not cursor.fetchone():
                return err(40401, "景点不存在")
            cursor.execute("INSERT INTO favorites(user_id, spot_id) VALUES(%s,%s)", (user["id"], spot_id))
        db.commit()
        return ok(msg="收藏成功")
    except pymysql.err.IntegrityError:
        db.rollback()
        return err(40901, "该景点已收藏")
    except Exception as exc:
        db.rollback()
        return err(50001, f"收藏失败：{exc}")


@router.delete("/{spot_id}")
def remove_favorite(spot_id: int, user=Depends(current_user), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM favorites WHERE user_id=%s AND spot_id=%s", (user["id"], spot_id))
            if cursor.rowcount == 0:
                return err(40401, "未收藏该景点")
        db.commit()
        return ok(msg="取消收藏成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"取消收藏失败：{exc}")
