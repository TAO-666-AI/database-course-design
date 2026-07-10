from difflib import SequenceMatcher
from typing import Optional


def match_faq(cursor, question: str) -> Optional[dict]:
    q = question.strip()
    if not q:
        return None

    cursor.execute(
        "SELECT id, question, answer, category, keywords FROM faqs WHERE question=%s LIMIT 1",
        (q,),
    )
    exact = cursor.fetchone()
    if exact:
        exact["score"] = 100
        return exact

    like = f"%{q}%"
    cursor.execute(
        """
        SELECT id, question, answer, category, keywords FROM faqs
        WHERE question LIKE %s OR answer LIKE %s OR keywords LIKE %s
        ORDER BY sort_order ASC LIMIT 1
        """,
        (like, like, like),
    )
    row = cursor.fetchone()
    if row:
        row["score"] = 80
        return row

    cursor.execute("SELECT id, question, answer, category, keywords FROM faqs")
    candidates = []
    for faq in cursor.fetchall():
        score = SequenceMatcher(None, q, faq["question"]).ratio() * 60
        keywords = [x.strip() for x in (faq.get("keywords") or "").split(",") if x.strip()]
        score += sum(15 for x in keywords if x in q or q in x)
        if score >= 45:
            faq["score"] = round(score, 2)
            candidates.append(faq)
    candidates.sort(key=lambda item: item["score"], reverse=True)
    return candidates[0] if candidates else None
