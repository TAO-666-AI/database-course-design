from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from utils.response import clean_rows, ok

router = APIRouter(prefix="/api/admin/chat-records", tags=["管理员-聊天记录"])


@router.get("")
def admin_chat_records(keyword: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = """
    SELECT c.id, c.session_id, c.role, c.content, c.source, c.created_at, u.username, u.phone
    FROM chat_records c
    JOIN users u ON c.user_id=u.id
    WHERE 1=1
    """
    params = []
    if keyword:
        sql += " AND (c.content LIKE %s OR u.username LIKE %s OR u.phone LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    sql += " ORDER BY c.created_at DESC LIMIT 200"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})
