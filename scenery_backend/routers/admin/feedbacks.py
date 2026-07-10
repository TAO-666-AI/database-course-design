from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from schemas.feedback import FeedbackStatusForm
from utils.response import check_choice, clean_row, clean_rows, err, ok

router = APIRouter(prefix="/api/admin/feedbacks", tags=["管理员-反馈管理"])


@router.get("")
def admin_feedbacks(status: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = """
    SELECT f.*, u.username, u.phone
    FROM feedbacks f
    JOIN users u ON f.user_id=u.id
    WHERE 1=1
    """
    params = []
    if status:
        sql += " AND f.status=%s"
        params.append(status)
    sql += " ORDER BY f.created_at DESC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.put("/{feedback_id}")
def admin_process_feedback(feedback_id: int, form: FeedbackStatusForm, _=Depends(current_admin), db=Depends(get_db)):
    check_choice(form.status, {"pending", "processed", "ignored"}, "status")
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE feedbacks SET status=%s, reply=%s, processed_at=NOW() WHERE id=%s",
                (form.status, form.reply, feedback_id),
            )
            if cursor.rowcount == 0:
                return err(40401, "反馈不存在")
        db.commit()
        return ok(msg="反馈处理成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"反馈处理失败：{exc}")


@router.get("/stats")
def admin_feedback_stats(_=Depends(current_admin), db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total, ROUND(AVG(rating),2) AS avg_rating FROM feedbacks")
        summary = cursor.fetchone()
        cursor.execute("SELECT type, COUNT(*) AS count, ROUND(AVG(rating),2) AS avg_rating FROM feedbacks GROUP BY type ORDER BY count DESC")
        by_type = cursor.fetchall()
        cursor.execute("SELECT status, COUNT(*) AS count FROM feedbacks GROUP BY status")
        by_status = cursor.fetchall()
    return ok({"summary": clean_row(summary), "by_type": clean_rows(by_type), "by_status": clean_rows(by_status)})
