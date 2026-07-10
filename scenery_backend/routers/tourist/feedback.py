from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_user
from schemas.feedback import FeedbackForm
from utils.response import clean_rows, err, ok

router = APIRouter(prefix="/api/feedback", tags=["反馈"])


@router.post("")
def submit_feedback(form: FeedbackForm, user=Depends(current_user), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO feedbacks(user_id, type, rating, content) VALUES(%s,%s,%s,%s)",
                (user["id"], form.type, form.rating, form.content),
            )
        db.commit()
        return ok(msg="反馈提交成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"反馈提交失败：{exc}")


@router.get("/mine")
def my_feedback(user=Depends(current_user), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, type, rating, content, status, reply, created_at, processed_at FROM feedbacks WHERE user_id=%s ORDER BY created_at DESC",
            (user["id"],),
        )
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})
