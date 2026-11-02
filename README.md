# 💰 SmartLedger - 智慧自訂記帳與預算監控系統

> **115-1 期中專題**：基於 Python 與 Streamlit 打造的高彈性、多維度自訂記帳與預算管理系統。

---

## 🌟 核心特色與亮點

1. **高度客製化 (Customization)**
   - **自訂收支分類**：可隨時新增、刪除分類，並為分類搭配專屬 Emoji 圖示（如 🍔 美食、🎬 娛樂、💼 薪資）。
   - **自訂支付管道/帳戶**：支援現金、銀行帳戶、悠遊卡、街口支付/Line Pay、信用卡等多帳戶管理，並設定起始金額。
2. **三色預算超支警示機制 (Budget & Alerts)**
   - 為各支出分類自訂月預算上限。
   - 即時計算預算消耗率，直觀呈現：
     - 🟢 **安全**（使用率 < 80%）
     - 🟡 **警戒**（使用率 80% ~ 100%）
     - 🔴 **超支警示**（使用率 > 100%，首頁儀表板彈出全域紅色警報）
3. **視覺化財務儀表板 (Plotly Interactive Charts)**
   - **分類支出環形圖 (Donut Chart)**：即時掌握各大類消費佔比。
   - **每日收支趨勢圖 (Daily Cash Flow Bar Chart)**：綠色代表收入、紅色代表支出。
   - **各帳戶動態餘額圖**：帳戶餘額 = 初始餘額 + 累計收入 - 累計支出。
4. **完整 CRUD 明細管理與搜尋**
   - 多條件篩選（收支類型、分類、帳戶）。
   - 快速刪除指定單筆交易。
5. **資料持久化與備份匯出**
   - 使用輕量且免安裝的 SQLite 本地資料庫，資料永不遺失。
   - 支援**一鍵匯出 CSV 檔案**，方便使用 Excel / Google Sheets 做更進一步的資料分析。
6. **高品質代碼工程**
   - 包含完整的單元測試套件 (`test_accounting.py`)。

---

## 📐 系統模組架構

```text
115-1_AIAB/
├── app.py               # Streamlit 網頁主介面（頁面切換、表單互動）
├── database.py          # SQLite 資料庫初始化、結構設計與種子資料
├── services.py          # 核心商業邏輯 (CRUD、預算警示指標、帳戶即時餘額計算)
├── charts.py            # Plotly 互動視覺化模組 (圓餅圖、趨勢圖、預算長條圖)
├── test_accounting.py   # 單元測試模組 (Unittest)
├── seed_demo_data.py    # 快速產生示範數據腳本 (供 Demo 簡報使用)
├── requirements.txt     # 套件相依清單
└── README.md            # 專題詳細說明文件
```

---

## 🚀 快速開始 (Getting Started)

### 1. 安裝環境套件
```bash
pip install -r requirements.txt
```

### 2. （選用）匯入 Demo 示範資料
若你想在第一次啟動時就看到漂亮的圖表與預算警示效果，可以先執行：
```bash
python seed_demo_data.py
```

### 3. 啟動 Streamlit 網頁應用程式
```bash
streamlit run app.py
```
啟動後，瀏覽器會自動開啟 `http://localhost:8501`。

### 4. 執行單元測試
```bash
python -m unittest test_accounting.py
```
