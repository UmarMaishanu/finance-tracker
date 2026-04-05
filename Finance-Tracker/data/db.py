import sqlite3
import os

DB_NAME = "financetracker.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            type        TEXT    NOT NULL,
            date        TEXT    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT    NOT NULL,
            limit_amount   REAL    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT NOT NULL,
            membership_id TEXT NOT NULL
        )
    """)

    # Seed transactions if empty
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        seed_transactions = [
            ("Groceries",     85.50,   "Food",          "expense", "2026-03-01"),
            ("Salary",        3000.00, "Salary",        "income",  "2026-03-01"),
            ("Netflix",       15.99,   "Entertainment", "expense", "2026-03-02"),
            ("Electric Bill", 120.00,  "Bills",         "expense", "2026-03-03"),
            ("Uber",          25.50,   "Transport",     "expense", "2026-03-04"),
            ("Freelance",     500.00,  "Salary",        "income",  "2026-03-05"),
            ("Coffee",        12.00,   "Food",          "expense", "2026-03-06"),
            ("Gym",           40.00,   "Health",        "expense", "2026-03-07"),
            ("Bonus",         200.00,  "Salary",        "income",  "2026-03-08"),
            ("Internet Bill", 60.00,   "Bills",         "expense", "2026-03-09"),
        ]
        cursor.executemany(
            "INSERT INTO transactions (description, amount, category, type, date) VALUES (?,?,?,?,?)",
            seed_transactions
        )

    # Seed budgets if empty
    cursor.execute("SELECT COUNT(*) FROM budgets")
    if cursor.fetchone()[0] == 0:
        seed_budgets = [
            ("Food",          300.00),
            ("Transport",     100.00),
            ("Entertainment",  50.00),
            ("Bills",         200.00),
            ("Health",        100.00),
        ]
        cursor.executemany(
            "INSERT INTO budgets (category, limit_amount) VALUES (?,?)",
            seed_budgets
        )

    # Seed members if empty
    cursor.execute("SELECT COUNT(*) FROM members")
    if cursor.fetchone()[0] == 0:
        seed_members = [
            ("Alice Johnson", "alice@email.com", "MBR-001"),
            ("Bob Smith",     "bob@email.com",   "MBR-002"),
            ("Carol White",   "carol@email.com", "MBR-003"),
        ]
        cursor.executemany(
            "INSERT INTO members (name, email, membership_id) VALUES (?,?,?)",
            seed_members
        )

    conn.commit()
    conn.close()