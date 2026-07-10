from fastapi import APIRouter, Depends

from db.connection import get_db
from utils.response import clean_row, clean_rows, err, ok

router = APIRouter(prefix="/api/spots", tags=["景点"])


@router.get("")
def list_spots(keyword: str = "", category: str = "", db=Depends(get_db)):
    sql = "SELECT * FROM spots WHERE status='active'"
    params = []
    if keyword:
        sql += " AND (name LIKE %s OR description LIKE %s OR location LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    if category:
        sql += " AND category=%s"
        params.append(category)
    sql += " ORDER BY id ASC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.get("/categories")
def spot_categories(db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT category
            FROM spots
            WHERE status='active' AND category IS NOT NULL AND category <> ''
            ORDER BY category ASC
            """
        )
        rows = cursor.fetchall()
    return ok({"items": [row["category"] for row in rows]})


@router.get("/{spot_id}")
def spot_detail(spot_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM spots WHERE id=%s AND status='active'", (spot_id,))
        row = cursor.fetchone()
    if not row:
        return err(40401, "景点不存在")
    return ok(clean_row(row))
