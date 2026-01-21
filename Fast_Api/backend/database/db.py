# backend/database/db.py
import pymysql
from contextlib import contextmanager
from backend.config import settings  # 假设你有配置文件

@contextmanager
def get_db_connection():
    connection = pymysql.connect(
        host=settings.DB_HOST or "localhost",
        port=settings.DB_PORT or 13306,
        user=settings.DB_USER or "root",
        password=settings.DB_PASSWORD or "abc123",
        database=settings.DB_NAME or "douban_movies",
        charset='utf8mb4',
        autocommit=True
    )
    try:
        yield connection
    finally:
        connection.close()

def execute_query(sql: str):
    """
    执行 SELECT 查询并返回字典列表
    """
    with get_db_connection() as conn:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()