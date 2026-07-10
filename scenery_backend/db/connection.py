import pymysql
from pymysql.cursors import DictCursor

from core.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def get_conn(use_db: bool = True):
    kwargs = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
        "autocommit": False,
    }
    if use_db:
        kwargs["database"] = DB_NAME
    return pymysql.connect(**kwargs)


def get_db():
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()
