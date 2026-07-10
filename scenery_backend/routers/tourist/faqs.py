from fastapi import APIRouter, Depends, Query

from db.connection import get_db
from services.faq_service import match_faq
from utils.response import ok

router = APIRouter(prefix="/api/faqs", tags=["FAQ"])


@router.get("")
def list_faqs(category: str = "", keyword: str = "", db=Depends(get_db)):
    sql = "SELECT id, question, answer, category, keywords, sort_order FROM faqs WHERE status='active'"
    params = []
    if category:
        sql += " AND category=%s"
        params.append(category)
    if keyword:
        sql += " AND (question LIKE %s OR answer LIKE %s OR keywords LIKE %s)"
        like = f"%{keyword}%"
        params.extend([like, like, like])
    sql += " ORDER BY sort_order ASC, id DESC"
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return ok({"items": rows, "total": len(rows)})


@router.get("/match")
def faq_match(q: str = Query(..., min_length=1, max_length=200), db=Depends(get_db)):
    with db.cursor() as cursor:
        faq = match_faq(cursor, q)
    if not faq:
        return ok({"matched": False, "faq": None, "score": 0})
    return ok({"matched": True, "faq": faq, "score": faq.get("score", 0)})
