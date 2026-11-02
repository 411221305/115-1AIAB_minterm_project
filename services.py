"""
services.py - 核心商業邏輯模組
負責處理記帳資料的增刪改查 (CRUD)、自訂分類與帳戶管理、預算監控計算、統計分析與 CSV 匯出匯入。
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from database import get_db, init_db

# 全域預設資料庫路徑，可於單元測試中切換
CURRENT_DB = None


def set_db_file(db_file: Optional[str]):
    """設定當前使用的資料庫檔案。"""
    global CURRENT_DB
    CURRENT_DB = db_file


# ==========================================
# 1. 自訂分類管理 (Categories)
# ==========================================

def get_categories(record_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """取得所有自訂分類列表，可依 'expense' 或 'income' 篩選。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        if record_type:
            cursor.execute(
                "SELECT id, name, type, icon FROM categories WHERE type = ? ORDER BY id ASC;",
                (record_type,),
            )
        else:
            cursor.execute("SELECT id, name, type, icon FROM categories ORDER BY type, id ASC;")
        return [dict(row) for row in cursor.fetchall()]


def add_category(name: str, record_type: str, icon: str = "🏷️") -> bool:
    """新增自訂分類。若同類型中名稱已存在則回傳 False。"""
    try:
        with get_db(CURRENT_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?);",
                (name.strip(), record_type, icon.strip()),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def delete_category(category_id: int) -> bool:
    """刪除分類（若分類有被紀錄引用，會依外鍵串聯刪除）。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?;", (category_id,))
        conn.commit()
        return cursor.rowcount > 0


# ==========================================
# 2. 自訂帳戶與資產管理 (Accounts)
# ==========================================

def get_accounts() -> List[Dict[str, Any]]:
    """取得所有帳戶列表。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, initial_balance FROM accounts ORDER BY id ASC;")
        return [dict(row) for row in cursor.fetchall()]


def add_account(name: str, initial_balance: float = 0.0) -> bool:
    """新增自訂帳戶。"""
    try:
        with get_db(CURRENT_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (name, initial_balance) VALUES (?, ?);",
                (name.strip(), float(initial_balance)),
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def delete_account(account_id: int) -> tuple[bool, str]:
    """刪除帳戶。若該帳戶已有交易紀錄，則拒絕刪除以維護資料一致性。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM records WHERE account_id = ?;", (account_id,))
        if cursor.fetchone()["count"] > 0:
            return False, "該帳戶已有記帳紀錄，無法刪除！"

        cursor.execute("DELETE FROM accounts WHERE id = ?;", (account_id,))
        conn.commit()
        return True, "刪除成功！"


def get_account_balances() -> List[Dict[str, Any]]:
    """
    計算並取得所有帳戶的當前動態即時餘額：
    即時餘額 = 初始餘額 + 總收入 - 總支出
    """
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                a.id,
                a.name,
                a.initial_balance,
                COALESCE(SUM(CASE WHEN r.type = 'income' THEN r.amount ELSE 0 END), 0) AS total_income,
                COALESCE(SUM(CASE WHEN r.type = 'expense' THEN r.amount ELSE 0 END), 0) AS total_expense
            FROM accounts a
            LEFT JOIN records r ON a.id = r.account_id
            GROUP BY a.id, a.name, a.initial_balance
            ORDER BY a.id ASC;
        """
        cursor.execute(query)
        result = []
        for row in cursor.fetchall():
            current_balance = row["initial_balance"] + row["total_income"] - row["total_expense"]
            result.append({
                "id": row["id"],
                "name": row["name"],
                "initial_balance": row["initial_balance"],
                "total_income": row["total_income"],
                "total_expense": row["total_expense"],
                "current_balance": current_balance,
            })
        return result


# ==========================================
# 3. 交易紀錄管理 (Records CRUD)
# ==========================================

def add_record(record_date: str, record_type: str, amount: float, category_id: int, account_id: int, note: str = "") -> bool:
    """新增一筆記帳紀錄。"""
    if amount <= 0:
        return False
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO records (record_date, type, amount, category_id, account_id, note)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (record_date, record_type, float(amount), category_id, account_id, note.strip()),
        )
        conn.commit()
        return True


def get_records(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    record_type: Optional[str] = None,
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
) -> pd.DataFrame:
    """依多種篩選條件查詢交易紀錄，並回傳格式化後的 pandas DataFrame。"""
    query = """
        SELECT 
            r.id,
            r.record_date,
            r.type,
            r.amount,
            c.name AS category_name,
            c.icon AS category_icon,
            a.name AS account_name,
            r.note,
            r.category_id,
            r.account_id
        FROM records r
        JOIN categories c ON r.category_id = c.id
        JOIN accounts a ON r.account_id = a.id
        WHERE 1=1
    """
    params = []

    if start_date:
        query += " AND r.record_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND r.record_date <= ?"
        params.append(end_date)
    if record_type:
        query += " AND r.type = ?"
        params.append(record_type)
    if category_id:
        query += " AND r.category_id = ?"
        params.append(category_id)
    if account_id:
        query += " AND r.account_id = ?"
        params.append(account_id)

    query += " ORDER BY r.record_date DESC, r.id DESC;"

    with get_db(CURRENT_DB) as conn:
        df = pd.read_sql_query(query, conn, params=params)
    return df


def delete_record(record_id: int) -> bool:
    """刪除指定的一筆記帳紀錄。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id = ?;", (record_id,))
        conn.commit()
        return cursor.rowcount > 0


def update_record(record_id: int, record_date: str, record_type: str, amount: float, category_id: int, account_id: int, note: str) -> bool:
    """更新指定的一筆記帳紀錄。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE records
            SET record_date = ?, type = ?, amount = ?, category_id = ?, account_id = ?, note = ?
            WHERE id = ?;
            """,
            (record_date, record_type, float(amount), category_id, account_id, note.strip(), record_id),
        )
        conn.commit()
        return cursor.rowcount > 0


# ==========================================
# 4. 預算設定與超支警示 (Budgets & Alerts)
# ==========================================

def get_budgets() -> List[Dict[str, Any]]:
    """取得所有自訂的月預算設定。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        query = """
            SELECT b.id, b.category_id, c.name AS category_name, c.icon AS category_icon, b.monthly_limit
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            ORDER BY b.monthly_limit DESC;
        """
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]


def set_budget(category_id: int, monthly_limit: float) -> bool:
    """新增或更新分類月預算。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO budgets (category_id, monthly_limit)
            VALUES (?, ?)
            ON CONFLICT(category_id) DO UPDATE SET monthly_limit = excluded.monthly_limit;
            """,
            (category_id, float(monthly_limit)),
        )
        conn.commit()
        return True


def delete_budget(budget_id: int) -> bool:
    """刪除特定分類的預算設定。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM budgets WHERE id = ?;", (budget_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_budget_status(year_month: str) -> List[Dict[str, Any]]:
    """
    計算指定月份 (YYYY-MM) 的預算執行狀態與超支警示指標：
    - status: 'safe' (安全 <80%), 'warning' (注意 80%~100%), 'danger' (超支 >100%)
    """
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                b.id AS budget_id,
                b.category_id,
                c.name AS category_name,
                c.icon AS category_icon,
                b.monthly_limit,
                COALESCE(SUM(r.amount), 0) AS spent
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            LEFT JOIN records r ON r.category_id = b.category_id 
                AND r.type = 'expense' 
                AND strftime('%Y-%m', r.record_date) = ?
            GROUP BY b.id, b.category_id, c.name, c.icon, b.monthly_limit
            ORDER BY (spent / b.monthly_limit) DESC;
        """
        cursor.execute(query, (year_month,))
        results = []
        for row in cursor.fetchall():
            limit = row["monthly_limit"]
            spent = row["spent"]
            remaining = limit - spent
            pct = (spent / limit * 100) if limit > 0 else 0.0

            if pct >= 100:
                status = "danger"
            elif pct >= 80:
                status = "warning"
            else:
                status = "safe"

            results.append({
                "budget_id": row["budget_id"],
                "category_id": row["category_id"],
                "category_name": row["category_name"],
                "category_icon": row["category_icon"],
                "monthly_limit": limit,
                "spent": spent,
                "remaining": remaining,
                "percentage": round(pct, 1),
                "status": status,
            })
        return results


# ==========================================
# 5. 統計分析計算 (Monthly Summary & Trends)
# ==========================================

def get_monthly_summary(year_month: str) -> Dict[str, float]:
    """取得指定月份的總收入、總支出與淨結餘。"""
    with get_db(CURRENT_DB) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) AS total_income,
                COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) AS total_expense
            FROM records
            WHERE strftime('%Y-%m', record_date) = ?;
        """
        cursor.execute(query, (year_month,))
        row = cursor.fetchone()
        income = row["total_income"]
        expense = row["total_expense"]
        return {
            "income": income,
            "expense": expense,
            "net": income - expense,
        }


def get_category_breakdown(year_month: str, record_type: str = "expense") -> pd.DataFrame:
    """取得指定月份、指定類型的分類佔比排行。"""
    query = """
        SELECT 
            c.name AS category_name,
            c.icon AS category_icon,
            SUM(r.amount) AS total_amount
        FROM records r
        JOIN categories c ON r.category_id = c.id
        WHERE r.type = ? AND strftime('%Y-%m', r.record_date) = ?
        GROUP BY c.id, c.name, c.icon
        ORDER BY total_amount DESC;
    """
    with get_db(CURRENT_DB) as conn:
        df = pd.read_sql_query(query, conn, params=(record_type, year_month))
    return df


def get_daily_trends(year_month: str) -> pd.DataFrame:
    """取得指定月份內每日的收入與支出走勢。"""
    query = """
        SELECT 
            record_date,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) AS expense,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) AS income
        FROM records
        WHERE strftime('%Y-%m', record_date) = ?
        GROUP BY record_date
        ORDER BY record_date ASC;
    """
    with get_db(CURRENT_DB) as conn:
        df = pd.read_sql_query(query, conn, params=(year_month,))
    return df


# ==========================================
# 6. CSV 備份匯出與匯入 (Import / Export)
# ==========================================

def export_records_to_csv() -> str:
    """匯出所有交易紀錄為 CSV 字串格式。"""
    df = get_records()
    if df.empty:
        return ""
    export_df = df[["record_date", "type", "category_name", "amount", "account_name", "note"]].copy()
    export_df.rename(columns={
        "record_date": "日期",
        "type": "類型",
        "category_name": "分類",
        "amount": "金額",
        "account_name": "帳戶",
        "note": "備註",
    }, inplace=True)
    return export_df.to_csv(index=False, encoding="utf-8-sig")
