from datetime import datetime
from decimal import Decimal
from typing import Optional


def ok(data=None, msg: str = "success") -> dict:
    return {"code": 200, "msg": msg, "data": data}


def err(code: int, msg: str, data=None) -> dict:
    return {"code": code, "msg": msg, "data": data}


def clean_row(row: Optional[dict]) -> Optional[dict]:
    if not row:
        return row
    for key, value in list(row.items()):
        if isinstance(value, datetime):
            row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, Decimal):
            row[key] = float(value)
    return row


def clean_rows(rows: list[dict]) -> list[dict]:
    return [clean_row(row) for row in rows]


def check_choice(value: str, choices: set[str], field_name: str):
    from fastapi import HTTPException

    if value not in choices:
        raise HTTPException(status_code=422, detail=f"{field_name} 取值不合法")
