import uuid

from services.deepseek_service import call_deepseek
from services.faq_service import match_faq


def create_chat_reply(cursor, user_id: int, question: str, session_id: str | None = None) -> dict:
    session_id = session_id or uuid.uuid4().hex
    if not session_id.replace("_", "").replace("-", "").isalnum() or not (16 <= len(session_id) <= 64):
        return {"ok": False, "code": 40001, "msg": "session_id 格式不正确"}

    cursor.execute(
        "INSERT INTO chat_records(session_id, user_id, role, content, source) VALUES(%s,%s,'user',%s,'user')",
        (session_id, user_id, question),
    )
    faq = match_faq(cursor, question)
    if faq:
        reply, source = faq["answer"], "faq"
    else:
        reply, source = call_deepseek(question)
    cursor.execute(
        "INSERT INTO chat_records(session_id, user_id, role, content, source) VALUES(%s,%s,'assistant',%s,%s)",
        (session_id, user_id, reply, source),
    )
    return {"ok": True, "session_id": session_id, "reply": reply, "source": source}
