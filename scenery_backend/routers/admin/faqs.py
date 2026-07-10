from fastapi import APIRouter, Depends

from db.connection import get_db
from dependencies.auth import current_admin
from schemas.faq import FAQForm
from utils.response import clean_rows, err, ok

router = APIRouter(prefix="/api/admin/faqs", tags=["管理员-FAQ管理"])


@router.get("")
def admin_faqs(keyword: str = "", _=Depends(current_admin), db=Depends(get_db)):
    sql = "SELECT * FROM faqs WHERE 1=1"
    params = []
    if keyword:
        sql += " AND (question LIKE %s OR answer LIKE %s OR keywords LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    sql += " ORDER BY sort_order ASC, id DESC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": clean_rows(rows), "total": len(rows)})


@router.post("")
def admin_create_faq(form: FAQForm, admin=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO faqs(question, answer, category, keywords, sort_order, created_by) VALUES(%s,%s,%s,%s,%s,%s)",
                (form.question, form.answer, form.category, form.keywords, form.sort_order, admin["id"]),
            )
            item_id = cursor.lastrowid
        db.commit()
        return ok({"id": item_id}, "FAQ 创建成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"FAQ 创建失败：{exc}")


@router.put("/{faq_id}")
def admin_update_faq(faq_id: int, form: FAQForm, _=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "UPDATE faqs SET question=%s, answer=%s, category=%s, keywords=%s, sort_order=%s WHERE id=%s",
                (form.question, form.answer, form.category, form.keywords, form.sort_order, faq_id),
            )
            if cursor.rowcount == 0:
                return err(40401, "FAQ 不存在")
        db.commit()
        return ok(msg="FAQ 更新成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"FAQ 更新失败：{exc}")


@router.delete("/{faq_id}")
def admin_delete_faq(faq_id: int, _=Depends(current_admin), db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM faqs WHERE id=%s", (faq_id,))
            if cursor.rowcount == 0:
                return err(40401, "FAQ 不存在")
        db.commit()
        return ok(msg="FAQ 删除成功")
    except Exception as exc:
        db.rollback()
        return err(50001, f"FAQ 删除失败：{exc}")
