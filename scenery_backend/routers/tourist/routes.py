from fastapi import APIRouter, Depends, Query

from db.connection import get_db
from services.route_service import build_route
from utils.response import err, ok

router = APIRouter(prefix="/api/routes", tags=["路线"])


@router.get("")
def list_routes(keyword: str = "", difficulty: str = "", db=Depends(get_db)):
    sql = "SELECT * FROM routes WHERE 1=1"
    params = []
    if keyword:
        sql += " AND (name LIKE %s OR description LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like])
    if difficulty:
        sql += " AND difficulty=%s"
        params.append(difficulty)
    sql += " ORDER BY duration_hours ASC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = [build_route(cursor, row) for row in cursor.fetchall()]
    return ok({"items": rows, "total": len(rows)})


@router.get("/recommend")
def recommend_route(hours: float = Query(2, ge=0), difficulty: str = "", db=Depends(get_db)):
    sql = "SELECT *, ABS(duration_hours - %s) AS gap FROM routes WHERE 1=1"
    params = [hours]
    if difficulty:
        sql += " AND difficulty=%s"
        params.append(difficulty)
    sql += " ORDER BY gap ASC LIMIT 1"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        route = cursor.fetchone()
        if not route:
            return err(40401, "暂无合适路线")
        route = build_route(cursor, route)
    return ok(route)


@router.get("/{route_id}")
def route_detail(route_id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM routes WHERE id=%s", (route_id,))
        route = cursor.fetchone()
        if not route:
            return err(40401, "路线不存在")
        route = build_route(cursor, route)
    return ok(route)
