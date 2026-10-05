import sys
import asyncio
from psycopg_pool import ConnectionPool
from langchain_postgres.v2.engine import PGEngine
from psycopg.rows import dict_row

MIN_CONNECTION_SIZE=1
MAX_CONNECTION_SIZE=10

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Database:
    def __init__(self, connection_string: str):
        self.pool = ConnectionPool(
            conninfo=connection_string,
            min_size=MIN_CONNECTION_SIZE,
            max_size=MAX_CONNECTION_SIZE,
        )

        lc_url = connection_string.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

        self.engine = PGEngine.from_connection_string(
            url=lc_url
        )

    def execute(self, sql: str, params: tuple = ()):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params)
                return max(cur.rowcount, 0)

    def fetch_one(self, sql: str, params: tuple = ()):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params)
                return cur.fetchone()

    def fetch_all(self, sql: str, params: tuple = ()):
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def close(self):
        self.pool.close()