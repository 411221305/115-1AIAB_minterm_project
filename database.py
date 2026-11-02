"""
database.py - 資料庫初始化與資料表定義模組
負責管理 SQLite 資料庫連線、自動建立資料表，以及初始化預設的分類與帳戶資料。
"""

import sqlite3
from typing import Optional
from contextlib import contextmanager

DB_FILE = "finance.db"


@contextmanager
def get_db(db_file: Optional[str] = None):
    """資料庫連線上下文管理器，確保每次操作後連線均被正確關閉。"""
    conn = sqlite3.connect(db_file or DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_file: Optional[str] = None):
    """
    初始化資料庫：建立 categories, accounts, records, budgets 等表格，
    若為初次建立，會自動填入基礎常用分類與帳戶種子資料。
    """
    with get_db(db_file) as conn:
        cursor = conn.cursor()

        # 1. 自訂收支分類表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
                icon TEXT DEFAULT '🏷️',
                UNIQUE(name, type)
            );
        """)

        # 2. 自訂帳戶/支付方式表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                initial_balance REAL DEFAULT 0.0
            );
        """)

        # 3. 交易明細表記錄
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_date TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
                amount REAL NOT NULL CHECK(amount > 0),
                category_id INTEGER NOT NULL,
                account_id INTEGER NOT NULL,
                note TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
                FOREIGN KEY (account_id) REFERENCES accounts (id) ON DELETE RESTRICT
            );
        """)

        # 4. 每月分類預算設定表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL UNIQUE,
                monthly_limit REAL NOT NULL CHECK(monthly_limit >= 0),
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            );
        """)

        # 檢查是否為空資料庫，若是則填入預設資料
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        if cursor.fetchone()["count"] == 0:
            default_categories = [
                # 支出分類
                ("餐飲美食", "expense", "🍔"),
                ("交通通勤", "expense", "🚌"),
                ("日常購物", "expense", "🛒"),
                ("休閒娛樂", "expense", "🎬"),
                ("居家水電", "expense", "🏠"),
                ("醫療保健", "expense", "💊"),
                ("學習進修", "expense", "📚"),
                ("其他支出", "expense", "📦"),
                # 收入分類
                ("薪資所得", "income", "💼"),
                ("兼職副業", "income", "💰"),
                ("投資理財", "income", "📈"),
                ("獎金禮物", "income", "🎁"),
                ("其他收入", "income", "✨"),
            ]
            cursor.executemany(
                "INSERT INTO categories (name, type, icon) VALUES (?, ?, ?);",
                default_categories,
            )

        cursor.execute("SELECT COUNT(*) as count FROM accounts")
        if cursor.fetchone()["count"] == 0:
            default_accounts = [
                ("現金錢包", 2000.0),
                ("銀行帳戶", 50000.0),
                ("信用卡", 0.0),
                ("悠遊卡/一卡通", 500.0),
                ("行動支付 (Line Pay / 街口)", 1000.0),
            ]
            cursor.executemany(
                "INSERT INTO accounts (name, initial_balance) VALUES (?, ?);",
                default_accounts,
            )

        conn.commit()


if __name__ == "__main__":
    init_db()
    print("✅ 資料庫初始化完成！")
