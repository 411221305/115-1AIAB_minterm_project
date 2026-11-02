"""
app.py - 自訂智慧記帳程式 (SmartLedger)
期中專題 Streamlit 主介面程式
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import database
import services
import charts

# ==========================================
# 頁面配置與初始化
# ==========================================
st.set_page_config(
    page_title="SmartLedger - 自訂智慧記帳",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 自動初始化資料庫（若首次啟動）
database.init_db()

# 自訂 CSS 樣式美化
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3498db;
    }
    .stAlert {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 側邊欄：導航與全域月份選擇
# ==========================================
st.sidebar.title("💰 SmartLedger")
st.sidebar.caption("客製化智慧記帳與預算管理系統")

menu = st.sidebar.radio(
    "功能導航",
    [
        "📊 財務儀表板",
        "✍️ 快速記帳",
        "📋 歷史明細管理",
        "🎯 預算設定與警示",
        "⚙️ 自訂分類與帳戶",
        "💾 資料匯出備份",
    ],
    index=0,
)

st.sidebar.divider()

# 月份篩選器 (用於儀表板與預算分析)
today = date.today()
current_year = today.year
current_month = today.month

col_y, col_m = st.sidebar.columns(2)
with col_y:
    selected_year = st.selectbox("年份", range(current_year - 5, current_year + 5), index=5)
with col_m:
    selected_month = st.selectbox("月份", range(1, 13), index=current_month - 1)

selected_ym = f"{selected_year:04d}-{selected_month:02d}"

st.sidebar.info(f"📅 當前統計週期：**{selected_ym}**")


# ==========================================
# 頁面 1: 📊 財務儀表板 (Dashboard)
# ==========================================
if menu == "📊 財務儀表板":
    st.title(f"📊 財務數據總覽 ({selected_ym})")

    # 1. 計算當月關鍵指標
    summary = services.get_monthly_summary(selected_ym)
    account_balances = services.get_account_balances()
    total_assets = sum(acc["current_balance"] for acc in account_balances)

    # 2. 超支即時警示橫幅
    budget_statuses = services.get_budget_status(selected_ym)
    over_budgets = [b for b in budget_statuses if b["status"] == "danger"]
    warn_budgets = [b for b in budget_statuses if b["status"] == "warning"]

    if over_budgets:
        warning_msg = "、".join([f"**{b['category_icon']} {b['category_name']}** (超支 NT$ {abs(b['remaining']):,.0f})" for b in over_budgets])
        st.error(f"🚨 **預算超支警示！** 本月以下分類已超出預算上限：{warning_msg}，請留意開支！")
    elif warn_budgets:
        st.warning(f"⚠️ **預算警戒提醒！** 有 {len(warn_budgets)} 個分類花費已達到 80% 以上，請注意控制預算。")

    # 3. 指標卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("本月總收入", f"NT$ {summary['income']:,.0f}", delta=None)
    with col2:
        st.metric("本月總支出", f"NT$ {summary['expense']:,.0f}", delta=None)
    with col3:
        net_val = summary["net"]
        st.metric("本月淨結餘", f"NT$ {net_val:,.0f}", delta=f"{net_val:,.0f}")
    with col4:
        st.metric("目前總資產淨值", f"NT$ {total_assets:,.0f}")

    st.divider()

    # 4. 雙欄互動圖表
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        category_df = services.get_category_breakdown(selected_ym, record_type="expense")
        st.plotly_chart(charts.make_category_pie_chart(category_df, f"{selected_ym} 支出分類佔比"), use_container_width=True)

    with chart_col2:
        daily_df = services.get_daily_trends(selected_ym)
        st.plotly_chart(charts.make_daily_trend_chart(daily_df), use_container_width=True)

    # 5. 預算進度與帳戶分佈
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.subheader("🎯 分類預算執行狀況")
        if budget_statuses:
            st.plotly_chart(charts.make_budget_progress_chart(budget_statuses), use_container_width=True)
        else:
            st.info("尚無設定預算，可至側邊欄「🎯 預算設定與警示」設定專屬預算！")

    with sub_col2:
        st.subheader("💳 各帳戶即時餘額")
        st.plotly_chart(charts.make_account_balance_chart(account_balances), use_container_width=True)


# ==========================================
# 頁面 2: ✍️ 快速記帳 (Add Record)
# ==========================================
elif menu == "✍️ 快速記帳":
    st.title("✍️ 新增記帳紀錄")
    st.write("記錄每一筆日常開銷或收入，系統將即時更新餘額與預算！")

    categories_expense = services.get_categories("expense")
    categories_income = services.get_categories("income")
    accounts = services.get_accounts()

    if not accounts:
        st.error("目前尚無任何帳戶，請先至「自訂分類與帳戶」頁面建立帳戶！")
    else:
        with st.form("record_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                r_type = st.radio("收支類型", ["支出 (Expense)", "收入 (Income)"], horizontal=True)
                actual_type = "expense" if "支出" in r_type else "income"

                target_categories = categories_expense if actual_type == "expense" else categories_income
                category_options = {f"{c['icon']} {c['name']}": c["id"] for c in target_categories}

                selected_cat_name = st.selectbox("選擇分類", list(category_options.keys()))
                selected_cat_id = category_options[selected_cat_name] if category_options else None

            with f_col2:
                amount = st.number_input("金額 (NT$)", min_value=1.0, value=100.0, step=10.0, format="%.0f")
                account_options = {acc["name"]: acc["id"] for acc in accounts}
                selected_acc_name = st.selectbox("選擇支付/存入帳戶", list(account_options.keys()))
                selected_acc_id = account_options[selected_acc_name]

            r_date = st.date_input("交易日期", value=date.today())
            note = st.text_input("備註說明 (選填)", placeholder="例如：午餐雞腿便當、7-11 咖啡...")

            submitted = st.form_submit_button("💾 儲存這筆紀錄", use_container_width=True)
            if submitted:
                if selected_cat_id is None:
                    st.error("請先建立對應分類！")
                else:
                    success = services.add_record(
                        record_date=r_date.strftime("%Y-%m-%d"),
                        record_type=actual_type,
                        amount=amount,
                        category_id=selected_cat_id,
                        account_id=selected_acc_id,
                        note=note,
                    )
                    if success:
                        st.success(f"🎉 記帳成功！【{r_type.split()[0]}】NT$ {amount:,.0f}（{selected_cat_name}）已記錄。")
                        st.balloons()
                    else:
                        st.error("儲存失敗，請檢查輸入數值！")

        # 顯示最近 5 筆紀錄
        st.subheader("🕒 最近 5 筆交易紀錄")
        recent_df = services.get_records().head(5)
        if not recent_df.empty:
            display_recent = recent_df[["record_date", "type", "category_icon", "category_name", "amount", "account_name", "note"]].copy()
            display_recent["分類"] = display_recent["category_icon"] + " " + display_recent["category_name"]
            display_recent["類型"] = display_recent["type"].map({"expense": "🔴 支出", "income": "🟢 收入"})
            display_recent["金額"] = display_recent["amount"].apply(lambda x: f"NT$ {x:,.0f}")
            display_recent.rename(columns={"record_date": "日期", "account_name": "帳戶", "note": "備註"}, inplace=True)
            st.dataframe(display_recent[["日期", "類型", "分類", "金額", "帳戶", "備註"]], use_container_width=True)


# ==========================================
# 頁面 3: 📋 歷史明細管理 (History & CRUD)
# ==========================================
elif menu == "📋 歷史明細管理":
    st.title("📋 交易紀錄明細與管理")

    # 篩選欄
    with st.expander("🔍 進階多條件篩選", expanded=True):
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            filter_type = st.selectbox("類型", ["全部", "支出", "收入"])
            f_type = "expense" if filter_type == "支出" else ("income" if filter_type == "收入" else None)
        with f_col2:
            all_cats = services.get_categories()
            cat_filter_map = {"全部": None}
            for c in all_cats:
                cat_filter_map[f"{c['icon']} {c['name']} ({c['type']})"] = c["id"]
            selected_filter_cat = st.selectbox("分類", list(cat_filter_map.keys()))
            f_cat_id = cat_filter_map[selected_filter_cat]
        with f_col3:
            all_accs = services.get_accounts()
            acc_filter_map = {"全部": None}
            for a in all_accs:
                acc_filter_map[a["name"]] = a["id"]
            selected_filter_acc = st.selectbox("帳戶", list(acc_filter_map.keys()))
            f_acc_id = acc_filter_map[selected_filter_acc]
        with f_col4:
            records_df = services.get_records(
                record_type=f_type,
                category_id=f_cat_id,
                account_id=f_acc_id,
            )
            st.metric("符合筆數", f"{len(records_df)} 筆")

    if records_df.empty:
        st.info("查無任何符合條件的記帳明細 🍃")
    else:
        # 顯示列表
        display_df = records_df.copy()
        display_df["分類"] = display_df["category_icon"] + " " + display_df["category_name"]
        display_df["類型"] = display_df["type"].map({"expense": "🔴 支出", "income": "🟢 收入"})
        display_df["金額"] = display_df["amount"].apply(lambda x: f"NT$ {x:,.0f}")
        display_df.rename(columns={"record_date": "日期", "account_name": "帳戶", "note": "備註", "id": "編號"}, inplace=True)

        st.dataframe(
            display_df[["編號", "日期", "類型", "分類", "金額", "帳戶", "備註"]],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("🗑️ 刪除指定紀錄")
        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
            record_id_to_del = st.selectbox("選擇要刪除的紀錄編號", records_df["id"].tolist())
        with del_col2:
            if st.button("確認刪除這筆紀錄", type="primary", use_container_width=True):
                if services.delete_record(record_id_to_del):
                    st.success(f"已成功刪除編號 {record_id_to_del} 的紀錄！")
                    st.rerun()


# ==========================================
# 頁面 4: 🎯 預算設定與警示 (Budgets & Alerts)
# ==========================================
elif menu == "🎯 預算設定與警示":
    st.title("🎯 每月分類預算與超支監控")
    st.write("設定每個支出類別的每月上限金額。當支出超過 80% 顯示黃色警戒，超過 100% 顯示紅色超支！")

    # 1. 預算設定表單
    expense_categories = services.get_categories("expense")
    if not expense_categories:
        st.warning("尚無支出分類可設定預算！")
    else:
        with st.form("set_budget_form"):
            b_col1, b_col2, b_col3 = st.columns([2, 2, 1])
            with b_col1:
                budget_cat_map = {f"{c['icon']} {c['name']}": c["id"] for c in expense_categories}
                b_cat_name = st.selectbox("支出分類", list(budget_cat_map.keys()))
                b_cat_id = budget_cat_map[b_cat_name]
            with b_col2:
                b_limit = st.number_input("每月預算上限 (NT$)", min_value=100.0, value=3000.0, step=500.0)
            with b_col3:
                st.write("")
                st.write("")
                submit_b = st.form_submit_button("設定 / 更新預算", use_container_width=True)

            if submit_b:
                services.set_budget(b_cat_id, b_limit)
                st.success(f"已成功設定 【{b_cat_name}】 的月預算為 NT$ {b_limit:,.0f}！")
                st.rerun()

    st.divider()

    # 2. 當月預算執行狀態列表
    st.subheader(f"📊 {selected_ym} 預算執行與超支監控")
    status_list = services.get_budget_status(selected_ym)

    if not status_list:
        st.info("目前尚未設定任何分類預算。請在上方表單新增！")
    else:
        for b in status_list:
            cat_display = f"{b['category_icon']} **{b['category_name']}**"
            limit_str = f"NT$ {b['monthly_limit']:,.0f}"
            spent_str = f"NT$ {b['spent']:,.0f}"
            rem_str = f"NT$ {b['remaining']:,.0f}"

            col_info, col_prog, col_btn = st.columns([3, 4, 1])
            with col_info:
                st.markdown(f"### {cat_display}")
                st.caption(f"預算上限：{limit_str} ｜ 已支出：{spent_str} ｜ 剩餘：{rem_str}")

            with col_prog:
                prog_val = min(1.0, max(0.0, b["spent"] / b["monthly_limit"]))
                if b["status"] == "danger":
                    st.error(f"🔴 已超出上限！使用率：{b['percentage']}% (超額 NT$ {abs(b['remaining']):,.0f})")
                elif b["status"] == "warning":
                    st.warning(f"🟡 警戒！已達 {b['percentage']}%")
                else:
                    st.success(f"🟢 正常進度：{b['percentage']}%")
                st.progress(prog_val)

            with col_btn:
                st.write("")
                if st.button("刪除預算", key=f"del_b_{b['budget_id']}"):
                    services.delete_budget(b["budget_id"])
                    st.rerun()
            st.divider()


# ==========================================
# 頁面 5: ⚙️ 自訂分類與帳戶 (Customization)
# ==========================================
elif menu == "⚙️ 自訂分類與帳戶":
    st.title("⚙️ 自訂分類與帳戶管理")
    st.write("自由擴充你的專屬收支分類與支付管道，打造個人化記帳工具！")

    tab1, tab2 = st.tabs(["🏷️ 自訂收支分類", "💳 自訂帳戶與資產"])

    # ------------------ Tab 1: 自訂收支分類 ------------------
    with tab1:
        st.subheader("新增自訂分類")
        with st.form("new_category_form", clear_on_submit=True):
            cat_c1, cat_c2, cat_c3 = st.columns([2, 1, 1])
            with cat_c1:
                new_cat_name = st.text_input("分類名稱", placeholder="例如：手搖飲料、寵物開銷、健身...")
            with cat_c2:
                new_cat_type = st.selectbox("收支類型", ["支出", "收入"])
                raw_type = "expense" if new_cat_type == "支出" else "income"
            with cat_c3:
                new_cat_icon = st.text_input("圖示 Emoji", value="🏷️")

            submit_cat = st.form_submit_button("新增分類", use_container_width=True)
            if submit_cat:
                if not new_cat_name.strip():
                    st.error("請輸入分類名稱！")
                else:
                    if services.add_category(new_cat_name, raw_type, new_cat_icon):
                        st.success(f"已成功新增分類：{new_cat_icon} {new_cat_name}！")
                        st.rerun()
                    else:
                        st.error("該分類名稱在此類型中已存在！")

        st.divider()
        st.subheader("現有分類清單")
        exp_col, inc_col = st.columns(2)
        with exp_col:
            st.markdown("#### 🔴 支出分類")
            expense_cats = services.get_categories("expense")
            for c in expense_cats:
                c_col1, c_col2 = st.columns([3, 1])
                c_col1.write(f"{c['icon']} {c['name']}")
                if c_col2.button("刪除", key=f"del_cat_{c['id']}"):
                    services.delete_category(c["id"])
                    st.rerun()

        with inc_col:
            st.markdown("#### 🟢 收入分類")
            income_cats = services.get_categories("income")
            for c in income_cats:
                c_col1, c_col2 = st.columns([3, 1])
                c_col1.write(f"{c['icon']} {c['name']}")
                if c_col2.button("刪除", key=f"del_cat_{c['id']}"):
                    services.delete_category(c["id"])
                    st.rerun()

    # ------------------ Tab 2: 自訂帳戶與資產 ------------------
    with tab2:
        st.subheader("新增自訂帳戶 / 支付管道")
        with st.form("new_account_form", clear_on_submit=True):
            acc_c1, acc_c2 = st.columns(2)
            with acc_c1:
                new_acc_name = st.text_input("帳戶名稱", placeholder="例如：玉山銀行、台新街口卡、美金帳戶...")
            with acc_c2:
                new_acc_init = st.number_input("初始餘額 (NT$)", value=0.0, step=100.0)

            submit_acc = st.form_submit_button("新增帳戶", use_container_width=True)
            if submit_acc:
                if not new_acc_name.strip():
                    st.error("請輸入帳戶名稱！")
                else:
                    if services.add_account(new_acc_name, new_acc_init):
                        st.success(f"已成功建立帳戶：{new_acc_name}！")
                        st.rerun()
                    else:
                        st.error("帳戶名稱已存在！")

        st.divider()
        st.subheader("現有帳戶列表與資產狀態")
        acc_balances = services.get_account_balances()
        for acc in acc_balances:
            a_col1, a_col2, a_col3, a_col4 = st.columns([2, 2, 2, 1])
            a_col1.markdown(f"🏦 **{acc['name']}**")
            a_col2.caption(f"初始餘額: NT$ {acc['initial_balance']:,.0f}")
            a_col3.markdown(f"**即時餘額: NT$ {acc['current_balance']:,.0f}**")
            if a_col4.button("刪除", key=f"del_acc_{acc['id']}"):
                ok, msg = services.delete_account(acc["id"])
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)


# ==========================================
# 頁面 6: 💾 資料匯出備份 (Export)
# ==========================================
elif menu == "💾 資料匯出備份":
    st.title("💾 資料匯出與備份管理")
    st.write("你可以將所有的記帳資料匯出為 CSV 試算表檔案，便於在 Excel 中進一步分析，或作為離線備份！")

    csv_data = services.export_records_to_csv()

    if csv_data:
        st.success("✅ 資料庫紀錄準備就緒，可隨時點擊下方按鈕下載！")
        st.download_button(
            label="📥 下載全部交易紀錄 (CSV 格式)",
            data=csv_data,
            file_name=f"finance_records_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()
        st.subheader("📄 預覽即將匯出的資料前 10 筆")
        preview_df = services.get_records().head(10)
        st.dataframe(preview_df[["record_date", "type", "category_name", "amount", "account_name", "note"]], use_container_width=True)
    else:
        st.info("目前資料庫中尚未有任何記帳紀錄，請先至「✍️ 快速記帳」輸入第一筆交易！")
