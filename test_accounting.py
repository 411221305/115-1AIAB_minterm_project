"""
test_accounting.py - 記帳程式單元測試模組
驗證資料庫建立、CRUD 核心邏輯、預算警示與餘額計算功能。
"""

import unittest
import os
import gc
import database
import services

TEST_DB = "test_finance.db"


class TestAccountingServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        services.set_db_file(TEST_DB)

    @classmethod
    def tearDownClass(cls):
        services.set_db_file(None)
        gc.collect()
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except OSError:
                pass

    def setUp(self):
        # 每次測試前重置資料庫
        gc.collect()
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except OSError:
                pass
        database.init_db(TEST_DB)

    def test_database_initialization(self):
        """測試資料庫是否成功自動填充預設分類與帳戶"""
        categories = services.get_categories()
        accounts = services.get_accounts()
        self.assertGreater(len(categories), 0)
        self.assertGreater(len(accounts), 0)

    def test_add_and_delete_category(self):
        """測試自訂分類的新增與刪除"""
        # 新增
        success = services.add_category("健身教練課", "expense", "🏋️")
        self.assertTrue(success)

        # 重複新增應失敗
        duplicate = services.add_category("健身教練課", "expense", "🏋️")
        self.assertFalse(duplicate)

        # 查詢
        categories = services.get_categories("expense")
        names = [c["name"] for c in categories]
        self.assertIn("健身教練課", names)

        # 刪除
        cat_id = [c["id"] for c in categories if c["name"] == "健身教練課"][0]
        del_success = services.delete_category(cat_id)
        self.assertTrue(del_success)

    def test_account_balance_calculation(self):
        """測試帳戶即時餘額動態計算：初始餘額 + 收入 - 支出"""
        services.add_account("測試帳戶", 1000.0)
        accounts = services.get_accounts()
        acc = [a for a in accounts if a["name"] == "測試帳戶"][0]
        acc_id = acc["id"]

        cat = services.get_categories("expense")[0]
        cat_inc = services.get_categories("income")[0]

        # 支出 200
        services.add_record("2026-10-15", "expense", 200.0, cat["id"], acc_id, "測試支出")
        # 收入 500
        services.add_record("2026-10-16", "income", 500.0, cat_inc["id"], acc_id, "測試收入")

        balances = services.get_account_balances()
        target_bal = [b for b in balances if b["id"] == acc_id][0]
        # 1000 + 500 - 200 = 1300
        self.assertEqual(target_bal["current_balance"], 1300.0)

    def test_budget_alert_levels(self):
        """測試預算警戒（安全、警戒 80%、超支 100%）"""
        cat = services.get_categories("expense")[0]
        acc = services.get_accounts()[0]

        # 設定預算上限為 1000 元
        services.set_budget(cat["id"], 1000.0)

        # 1. 支出 500 元 -> 安全 (50%)
        services.add_record("2026-10-01", "expense", 500.0, cat["id"], acc["id"])
        status = services.get_budget_status("2026-10")
        target_b = [b for b in status if b["category_id"] == cat["id"]][0]
        self.assertEqual(target_b["status"], "safe")

        # 2. 再支出 350 元 -> 總支出 850 元 -> 警戒 (85%)
        services.add_record("2026-10-02", "expense", 350.0, cat["id"], acc["id"])
        status = services.get_budget_status("2026-10")
        target_b = [b for b in status if b["category_id"] == cat["id"]][0]
        self.assertEqual(target_b["status"], "warning")

        # 3. 再支出 200 元 -> 總支出 1050 元 -> 超支 (105%)
        services.add_record("2026-10-03", "expense", 200.0, cat["id"], acc["id"])
        status = services.get_budget_status("2026-10")
        target_b = [b for b in status if b["category_id"] == cat["id"]][0]
        self.assertEqual(target_b["status"], "danger")


if __name__ == "__main__":
    unittest.main()
