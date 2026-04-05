from models.transaction import Transaction
from models.budget import Budget
from models.member import Member
from data.db import get_connection


# ================================================================
# TRANSACTIONS
# ================================================================

def get_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, category, type, date FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return [Transaction(id=r[0], description=r[1], amount=r[2], category=r[3], transaction_type=r[4], date=r[5]) for r in rows]

def add_transaction(t: Transaction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (description, amount, category, type, date) VALUES (?,?,?,?,?)",
        (t.description, t.amount, t.category, t.transaction_type, t.date)
    )
    conn.commit()
    conn.close()

def update_transaction(transaction_id: int, t: Transaction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE transactions SET description=?, amount=?, category=?, type=?, date=? WHERE id=?",
        (t.description, t.amount, t.category, t.transaction_type, t.date, transaction_id)
    )
    conn.commit()
    conn.close()

def delete_transaction(transaction_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()

def search_transactions(query="", category=None, transaction_type=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, description, amount, category, type, date FROM transactions WHERE 1=1"
    params = []
    if query:
        sql += " AND (LOWER(description) LIKE ? OR LOWER(category) LIKE ? OR date LIKE ?)"
        v = f"%{query.strip().lower()}%"
        params.extend([v, v, v])
    if category and category != "All":
        sql += " AND category = ?"
        params.append(category)
    if transaction_type and transaction_type != "All":
        sql += " AND type = ?"
        params.append(transaction_type)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [Transaction(id=r[0], description=r[1], amount=r[2], category=r[3], transaction_type=r[4], date=r[5]) for r in rows]

def get_income():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, category, type, date FROM transactions WHERE type='income'")
    rows = cursor.fetchall()
    conn.close()
    return [Transaction(id=r[0], description=r[1], amount=r[2], category=r[3], transaction_type=r[4], date=r[5]) for r in rows]

def get_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, amount, category, type, date FROM transactions WHERE type='expense'")
    rows = cursor.fetchall()
    conn.close()
    return [Transaction(id=r[0], description=r[1], amount=r[2], category=r[3], transaction_type=r[4], date=r[5]) for r in rows]

def get_total_income():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='income'")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_total_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type='expense'")
    result = cursor.fetchone()[0]
    conn.close()
    return result

def get_net_balance():
    return get_total_income() - get_total_expenses()

def get_spent_for_category(category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE category=? AND type='expense'",
        (category,)
    )
    result = cursor.fetchone()[0]
    conn.close()
    return result


# ================================================================
# BUDGETS
# ================================================================

def get_budgets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, limit_amount FROM budgets")
    rows = cursor.fetchall()
    conn.close()
    return [Budget(id=r[0], category=r[1], limit=r[2]) for r in rows]

def add_budget(b: Budget):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO budgets (category, limit_amount) VALUES (?,?)",
        (b.category, b.limit)
    )
    conn.commit()
    conn.close()

def update_budget(budget_id: int, b: Budget):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE budgets SET category=?, limit_amount=? WHERE id=?",
        (b.category, b.limit, budget_id)
    )
    conn.commit()
    conn.close()

def delete_budget(budget_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE id=?", (budget_id,))
    conn.commit()
    conn.close()

def search_budgets(query=""):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, category, limit_amount FROM budgets WHERE 1=1"
    params = []
    if query:
        sql += " AND LOWER(category) LIKE ?"
        params.append(f"%{query.strip().lower()}%")
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [Budget(id=r[0], category=r[1], limit=r[2]) for r in rows]


# ================================================================
# MEMBERS
# ================================================================

def get_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, membership_id FROM members")
    rows = cursor.fetchall()
    conn.close()
    return [Member(id=r[0], name=r[1], email=r[2], membership_id=r[3]) for r in rows]

def add_member(m: Member):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO members (name, email, membership_id) VALUES (?,?,?)",
        (m.name, m.email, m.membership_id)
    )
    conn.commit()
    conn.close()

def update_member(member_id: int, m: Member):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE members SET name=?, email=?, membership_id=? WHERE id=?",
        (m.name, m.email, m.membership_id, member_id)
    )
    conn.commit()
    conn.close()

def delete_member(member_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
    conn.commit()
    conn.close()