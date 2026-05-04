import sqlite3

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
            date        TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'pending'
        )
    """)

    # Safely add status column if upgrading from older DB
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'")
    except:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            category     TEXT    NOT NULL,
            limit_amount REAL    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL,
            membership_id TEXT    NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member_budgets (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id   TEXT    NOT NULL UNIQUE,
            membership_id   TEXT    NOT NULL,
            category        TEXT    NOT NULL,
            assigned_limit  REAL    NOT NULL,
            start_date      TEXT    NOT NULL,
            active          INTEGER NOT NULL DEFAULT 1
        )
    """)

    # Seed transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO transactions (description, amount, category, type, date, status) VALUES (?,?,?,?,?,?)",
            [
                ("Groceries",     85.50,   "Food",          "expense", "2026-03-01", "confirmed"),
                ("Salary",        3000.00, "Salary",        "income",  "2026-03-01", "confirmed"),
                ("Netflix",       15.99,   "Entertainment", "expense", "2026-03-02", "confirmed"),
                ("Electric Bill", 120.00,  "Bills",         "expense", "2026-03-03", "confirmed"),
                ("Uber",          25.50,   "Transport",     "expense", "2026-03-04", "confirmed"),
                ("Freelance",     500.00,  "Salary",        "income",  "2026-03-05", "confirmed"),
                ("Coffee",        12.00,   "Food",          "expense", "2026-03-06", "pending"),
                ("Gym",           40.00,   "Health",        "expense", "2026-03-07", "pending"),
                ("Bonus",         200.00,  "Salary",        "income",  "2026-03-08", "pending"),
                ("Internet Bill", 60.00,   "Bills",         "expense", "2026-03-09", "pending"),
            ]
        )

    # Seed budgets
    cursor.execute("SELECT COUNT(*) FROM budgets")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO budgets (category, limit_amount) VALUES (?,?)",
            [
                ("Food",          300.00),
                ("Transport",     100.00),
                ("Entertainment",  50.00),
                ("Bills",         200.00),
                ("Health",        100.00),
            ]
        )

    conn.commit()
    conn.close()