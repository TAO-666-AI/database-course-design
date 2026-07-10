from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_user
from schemas.chat import ChatForm
from services.chat_service import create_chat_reply
from utils.response import clean_rows, err, ok

router = APIRouter(prefix="/api/chat", tags=["文本问答"])


@router.post("")
def chat(form: ChatForm, user=Depends(current_user), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            result = create_chat_reply(cursor, user["id"], form.question.strip(), form.session_id)
            if not result["ok"]:
                return err(result["code"], result["msg"])
        db.commit()
        return ok({"session_id": result["session_id"], "reply": result["reply"], "source": result["source"]})
    except Exception as exc:
        db.rollback()
        return err(50001, f"问答失败：{exc}")


@router.get("/history")
def chat_history(user=Depends(current_user), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT session_id, MIN(created_at) AS started_at, MAX(created_at) AS updated_at, COUNT(*) AS message_count
            FROM chat_records
            WHERE user_id=%s
            GROUP BY session_id
            ORDER BY updated_at DESC
            """,
            (user["id"],),
        )
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute(
                "SELECT content FROM chat_records WHERE user_id=%s AND session_id=%s AND role='user' ORDER BY created_at ASC LIMIT 1",
                (user["id"], row["session_id"]),
            )
            first = cursor.fetchone()
            row["title"] = first["content"][:30] if first else "新会话"
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.get("/history/{session_id}")
def chat_history_detail(session_id: str, user=Depends(current_user), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT role, content, source, created_at FROM chat_records WHERE user_id=%s AND session_id=%s ORDER BY created_at ASC",
            (user["id"], session_id),
        )
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})
