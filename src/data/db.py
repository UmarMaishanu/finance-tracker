import sqlite3
from pathlib import Path
from .schema import BOOKS_TABLE_SQL

def db_path() -> Path:
    #DB stored in project root for now (we'll improve this later )
    return Path(__file__).resolve().parents[2] /"library.db"
    
def connect():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn

def ini_db():
    with connect() as conn:
        conn.execute(BOOKS_TABLE_SQL)

        def seed_if_empty():
            with connect() as conn:
                c = conn.execute("SELECT COUNT(*) AS n FROM books").fetchone()["n"]
                if c == 0:
                    conn.execute("INSERT INTO books(title, author,k)")
        