"""
seed_demo_data.py - 匯入示範資料腳本
為當前月份產生範例收支紀錄與預算設定，方便期中專題 Demo 展示豐富的圖表效果！
"""

from datetime import date, timedelta
import random
import database
import services

def seed():
    database.init_db()
    
    today = date.today()
    this_month_str = today.strftime("%Y-%m")
    
    # 取得分類與帳戶
    categories = services.get_categories()
    accounts = services.get_accounts()
    
    cat_by_name = {c["name"]: c["id"] for c in categories}
    acc_by_name = {a["name"]: a["id"] for a in accounts}
    
    # 1. 設定預算示範
    if "餐飲美食" in cat_by_name:
        services.set_budget(cat_by_name["餐飲美食"], 6000.0)
    if "交通通勤" in cat_by_name:
        services.set_budget(cat_by_name["交通通勤"], 1500.0)
    if "休閒娛樂" in cat_by_name:
        services.set_budget(cat_by_name["休閒娛樂"], 2000.0)
    if "日常購物" in cat_by_name:
        services.set_budget(cat_by_name["日常購物"], 3000.0)

    # 2. 建立一些本月的收支範例紀錄
    sample_records = [
        # (天數位移, 類型, 金額, 分類, 帳戶, 備註)
        (-15, "income", 38000.0, "薪資所得", "銀行帳戶", "十月份正職薪資入帳"),
        (-12, "income", 3500.0, "兼職副業", "銀行帳戶", "專案設計外包收入"),
        (-14, "expense", 1280.0, "交通通勤", "悠遊卡/一卡通", "悠遊卡定期票加值"),
        (-13, "expense", 150.0, "餐飲美食", "現金錢包", "午餐拉麵套餐"),
        (-11, "expense", 85.0, "餐飲美食", "行動支付 (Line Pay / 街口)", "早餐咖啡與三明治"),
        (-10, "expense", 2400.0, "休閒娛樂", "信用卡", "朋友聚餐唱歌派對"),
        (-8, "expense", 680.0, "日常購物", "信用卡", "生活用品補充 (沐浴乳、衛生紙)"),
        (-7, "expense", 220.0, "餐飲美食", "現金錢包", "晚餐牛排定食"),
        (-5, "expense", 450.0, "學習進修", "信用卡", "購買 Python 專業技術書籍"),
        (-3, "expense", 180.0, "餐飲美食", "行動支付 (Line Pay / 街口)", "下午茶甜點與手搖飲"),
        (-1, "expense", 320.0, "餐飲美食", "信用卡", "週末火鍋便當"),
        (0, "expense", 90.0, "餐飲美食", "現金錢包", "今日午餐排骨飯"),
    ]
    
    for offset, r_type, amount, cat_name, acc_name, note in sample_records:
        rec_date = (today + timedelta(days=offset)).strftime("%Y-%m-%d")
        if cat_name in cat_by_name and acc_name in acc_by_name:
            services.add_record(
                record_date=rec_date,
                record_type=r_type,
                amount=amount,
                category_id=cat_by_name[cat_name],
                account_id=acc_by_name[acc_name],
                note=note
            )
            
    print("✅ 示範資料填充完成！已包含預算設定與多筆收支交易。")

if __name__ == "__main__":
    seed()
