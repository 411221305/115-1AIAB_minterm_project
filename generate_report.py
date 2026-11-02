# -*- coding: utf-8 -*-
"""
generate_report.py
產生期中專題 Word 報告 (.docx)
涵蓋五大核心要求：
1. 這個專案做什麼 (Project Overview & Features)
2. 給誰用 (Target Audience & User Personas)
3. 怎麼跟 AI 一起做 (Human-AI Collaboration Process)
4. 查了什麼 (Research, Technical Selection & References)
5. 下一步 (Future Roadmap & Expansion)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """設定儲存格背景底色"""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """設定儲存格內距 (dxa)"""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_run(run, font_name="微軟正黑體", size_pt=11, bold=False, color_rgb=(51, 51, 51), italic=False):
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        if level == 1:
            format_run(r, font_name="微軟正黑體", size_pt=16, bold=True, color_rgb=(26, 82, 118)) # 深深藍
        elif level == 2:
            format_run(r, font_name="微軟正黑體", size_pt=13, bold=True, color_rgb=(41, 128, 185)) # 典雅藍
        elif level == 3:
            format_run(r, font_name="微軟正黑體", size_pt=11.5, bold=True, color_rgb=(52, 73, 94))
    return h

def add_body_paragraph(doc, text="", space_after=6, line_spacing=1.2, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, font_name="微軟正黑體", size_pt=11, bold=True, color_rgb=(44, 62, 80))
    if text:
        r = p.add_run(text)
        format_run(r, font_name="微軟正黑體", size_pt=11, bold=False, color_rgb=(51, 51, 51))
    return p

def add_bullet_item(doc, bold_title, content):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(bold_title)
    format_run(r_title, font_name="微軟正黑體", size_pt=11, bold=True, color_rgb=(44, 62, 80))
    r_content = p.add_run(content)
    format_run(r_content, font_name="微軟正黑體", size_pt=11, bold=False, color_rgb=(51, 51, 51))
    return p

def build_word_report(output_filename="期中專題報告_SmartLedger自訂記帳系統.docx"):
    doc = docx.Document()
    
    # 邊界設定 (標準 1 英吋)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # 封面/大標題
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("期中專題成果報告書\nSmartLedger：可自訂義智慧記帳與預算監控系統")
    format_run(r_title, font_name="微軟正黑體", size_pt=22, bold=True, color_rgb=(26, 82, 118))

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(20)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("基於 Python、Streamlit 與 SQLite 之人機協同軟體工程實踐")
    format_run(r_sub, font_name="微軟正黑體", size_pt=13, italic=True, color_rgb=(100, 110, 120))

    # 基本資訊卡片表格
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("課程名稱", "人工智慧與應用 / 軟體工程專案實作 (115-1)"),
        ("專案名稱", "SmartLedger 智慧自訂記帳系統"),
        ("核心技術棧", "Python 3.13、Streamlit、SQLite3、Plotly、Pandas"),
        ("協同開發工具", "Antigravity AI Agent (Pair Programming 人機協作)")
    ]
    for idx, (k, v) in enumerate(meta):
        c1, c2 = info_table.rows[idx].cells
        c1.width = Inches(1.8)
        c2.width = Inches(4.5)
        set_cell_background(c1, "EAECEE")
        set_cell_background(c2, "F8F9FA")
        set_cell_margins(c1, 80, 80, 120, 120)
        set_cell_margins(c2, 80, 80, 120, 120)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(k)
        format_run(r1, font_name="微軟正黑體", size_pt=10.5, bold=True, color_rgb=(44, 62, 80))
        
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(v)
        format_run(r2, font_name="微軟正黑體", size_pt=10.5, bold=False, color_rgb=(51, 51, 51))

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================================
    # 壹、這個專案做什麼 (Project Overview & Core Features)
    # ==========================================================
    add_styled_heading(doc, "壹、這個專案做什麼 (專案概述與核心功能)", level=1)
    
    add_body_paragraph(doc, 
        "現今市面上的記帳 App 多半存在「分類固定難以微調」、「支付通路無法貼合個人習慣（如悠遊卡、街口支付與特定銀行帳戶拆分）」以及「缺乏主動防呆與直觀超支警示」等痛點。使用者常常記了帳卻不知道錢流向何處，甚至到了月底才發現預算嚴重透支。"
    )
    add_body_paragraph(doc,
        "本專案「SmartLedger」是一款基於 Python 與 Streamlit 打造的現代化全功能 Web 記帳與個人財務管理系統。核心主軸圍繞在「高彈性自訂義（Customization）」與「主動式預算警示（Active Budget Control）」，結合 SQLite 本地持久化資料庫與 Plotly 互動式視覺化分析，讓使用者能夠隨心所欲打造專屬的財務儀表板。"
    )

    add_styled_heading(doc, "1. 系統六大核心模組與功能亮點", level=2)
    add_bullet_item(doc, "多維度自訂義（收支分類與 Emoji 標籤）：", "使用者不再受限於系統預設項目，可自由建立專屬支出與收入類別，並搭配客製化 Emoji 圖示（如 🍔 美食、🚌 通勤、📈 投資、🎁 獎金），提升日常記帳之視覺直覺性。")
    add_bullet_item(doc, "多帳戶與動態資產餘額追蹤：", "支援現金錢包、信用卡、銀行帳戶、悠遊卡、行動支付（Line Pay、街口）等多管道獨立記帳。系統後端自動計算每個帳戶的即時動態結餘：當前餘額 = 初始餘額 + 累計收入 - 累計支出。")
    add_bullet_item(doc, "三段式預算防線與智慧超支警示：", "為各個消費分類單獨設定「月預算上限」。系統動態計算預算消耗比率，分為安全（<80%，綠色）、警戒（80%~100%，黃色）、超支（>100%，紅色）。首頁儀表板在發生超支時會即時跳出全域警報橫幅，精確顯示超支金額。")
    add_bullet_item(doc, "Plotly 互動式圖表儀表板：", "提供支出分類環形圖（Donut Chart）、每日收支對比柱狀圖、帳戶資產分佈圖及預算進度條，支援滑鼠懸停數值探索、縮放與篩選，大幅優化財務洞察體驗。")
    add_bullet_item(doc, "多條件交易歷史明細查詢 (CRUD)：", "支援依類型（支出/收入）、特定分類、支付帳戶等多維度交叉篩選，並提供單筆記錄刪除功能，確保記帳資料整潔與正確。")
    add_bullet_item(doc, "資料持久化與一鍵 CSV 備份匯出：", "底層採用輕量且可靠的 SQLite 資料庫引擎，不需架設外部資料庫伺服器；並提供一鍵匯出繁體中文 UTF-8 附 BOM 的 CSV 檔案，可直接於 Excel / Google Sheets 進行深入統計分析。")

    add_styled_heading(doc, "2. 系統架構與代碼分工", level=2)
    add_body_paragraph(doc, "本專案在架構設計上嚴格遵循軟體工程「關注點分離（Separation of Concerns）」原則，劃分為五大模組，代碼耦合度低且維護性極高：")
    
    # 架構表格
    arch_table = doc.add_table(rows=6, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["模組檔案", "職責描述 (Role & Responsibility)", "關鍵技術 / 實作重點"]
    for i, h in enumerate(headers):
        c = arch_table.rows[0].cells[i]
        set_cell_background(c, "2C3E50")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        format_run(r, font_name="微軟正黑體", size_pt=10, bold=True, color_rgb=(255, 255, 255))
        
    modules_info = [
        ("app.py", "前端 Web 主應用程式", "Streamlit 側邊欄導航、表單驗證、全域月份選擇器、動態指標卡片"),
        ("database.py", "資料庫連線與結構管理", "SQLite3 外鍵約制開啟、自動建表 (Schema DDL)、常用分類帳戶種子資料填充"),
        ("services.py", "商業邏輯層 (Business Logic)", "交易明細增刪改查 (CRUD)、預算消耗比例計算、即時帳戶資產計算、CSV 格式轉換"),
        ("charts.py", "視覺化圖表引擎", "Plotly Express 與 Graph Objects 互動式環形圖、每日金流趨勢圖、預算警戒條形圖"),
        ("test_accounting.py", "自動化單元測試", "Python unittest 模組，涵蓋 CRUD、預算警戒判定、餘額計算之獨立沙盒測試")
    ]
    for row_idx, row_data in enumerate(modules_info, start=1):
        for col_idx, text in enumerate(row_data):
            cell = arch_table.rows[row_idx].cells[col_idx]
            bg = "FFFFFF" if row_idx % 2 == 1 else "F2F4F4"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            format_run(r, font_name="微軟正黑體", size_pt=9.5, color_rgb=(51, 51, 51), bold=(col_idx==0))

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================================
    # 貳、給誰用 (Target Audience & User Personas)
    # ==========================================================
    add_styled_heading(doc, "貳、給誰用 (目標使用者輪廓與應用情境)", level=1)
    add_body_paragraph(doc, "SmartLedger 針對不同生活與消費情境的個人與族群進行了專門的功能對標設計：")

    add_bullet_item(doc, "目標受眾一：大專院校學生與實習生", "學生族群通常可支配預算有限（如每月固定零用錢或打工薪資），容易在手搖飲、外食及社交聚會上無意識超支。透過自訂「外食」、「社團社交」分類與月預算上限，當月支出超過 80% 時即刻警示，能有效培養理性財務觀念。")
    add_bullet_item(doc, "目標受眾二：剛入職場的社會新鮮人 (小資族)", "薪水入帳後需要做好「薪資三分法」或「六罐子理財法」。系統支援分別追蹤「薪資帳戶」、「生活開銷卡」與「定期儲蓄帳戶」，透過清晰的月淨結餘（Net Flow）統計，清楚掌握每月能儲蓄並投資的實際金額。")
    add_bullet_item(doc, "目標受眾三：多元支付重度使用者 (Cashless Payers)", "現代人常穿梭於現金、信用卡、Line Pay、街口、悠遊卡等多種通路。傳統記帳軟體往往只能記單筆數字，SmartLedger 記錄時綁定特定支付管道，動態核算各卡片餘額，避免信用卡被刷爆或悠遊卡忘記儲值。")
    add_bullet_item(doc, "目標受眾四：兼職接案者與自由工作者 (Freelancers)", "收入時間與來源不固定（專案外包、版稅、獎金等）。透過自訂多種收入分類與月份歷史篩選，能清楚回顧各季度各類型副業收入之變化趨勢，協助報稅與年終收益檢討。")

    # ==========================================================
    # 參、怎麼跟 AI 一起做 (Human-AI Collaboration Process)
    # ==========================================================
    add_styled_heading(doc, "參、怎麼跟 AI 一起做 (人機協同軟體開發歷程)", level=1)
    add_body_paragraph(doc, 
        "本專案並非由人類單向編寫，亦非由 AI 盲目全自動生成，而是採用現代軟體工程推崇的「AI 結對編程（AI Pair Programming）」人機協同開發工作流。人類擔任『專案架構師與產品經理（Tech Lead / PM）』，AI（Antigravity）則擔任『高級全端工程師與軟體測試員』，雙方透過緊密的迭代循環推進專案："
    )

    add_styled_heading(doc, "1. 需求訪談與架構藍圖制定 (Planning & Inception)", level=2)
    add_body_paragraph(doc,
        "在專案初期，人類提出「想要做一個可以自訂義的期中記帳專題」之核心願景。AI 主動分析專案背景並提出引導式架構評估（如網頁版 Streamlit、桌面版 PyQt 與終端版 CLI 之優缺點比較）。經人類決策採用 Streamlit 後，AI 進一步收斂需求，將功能拆解為「分類管理」、「多帳戶資產」、「三色預算監控」、「互動圖表」與「CSV 備份」五大功能點，並繪製出明確的開發路線圖（Roadmap）。"
    )

    add_styled_heading(doc, "2. 資料庫實體關聯設計 (ERD & Database Schema)", level=2)
    add_body_paragraph(doc,
        "為支持高度自訂義，人類與 AI 討論出關聯式資料庫正規化設計。AI 快速設計出包含 categories (分類)、accounts (帳戶)、records (交易) 與 budgets (預算) 的 SQLite Schema，並開啟外鍵約束 (PRAGMA foreign_keys = ON) 與串聯刪除 (ON DELETE CASCADE)。AI 亦貼心編寫了自動檢測與填充預設資料（種子資料）機制，解決使用者首次進入系統面臨空白冷啟動（Cold-Start）的問題。"
    )

    add_styled_heading(doc, "3. 模組化編程與商業邏輯實現 (Services & Charts)", level=2)
    add_body_paragraph(doc,
        "在實作階段，人類負責驗收功能介面邏輯，AI 則負責撰寫高內聚、低耦合的 services.py 與 charts.py。過程中 AI 實作了強韌的例外處理，例如：\n"
        "• 在刪除帳戶時，主動檢查是否存在已記錄的交易，若有則阻止刪除以維持參照完整性（Referential Integrity）。\n"
        "• 在繪製 Plotly 圖表時，實作零資料/空資料守護機制（Zero-data Fallback），避免圖表拋出例外導致 Streamlit 頁面崩潰。"
    )

    add_styled_heading(doc, "4. 協同除錯與 Windows 檔案鎖定問題突破 (Debugging & Problem Solving)", level=2)
    add_body_paragraph(doc,
        "在編寫單元測試 (test_accounting.py) 時，曾遭遇 Windows 作業系統特有的「WinError 32: 程序無法存取檔案，因為檔案正由另一個程序使用」檔案鎖死報錯。人類與 AI 共同分析原因，發現舊有的連線寫法在連線未及時關閉時便嘗試刪除暫存測試資料庫。AI 迅速重構 database.py，引進 Python contextmanager (上下文管理器) 與 get_db() 生成器，確保連線在 with 區塊結束後百分之百被釋放，搭配垃圾回收機制 gc.collect()，成功使 4 項單元測試全數順利綠燈通過（100% Pass）。"
    )

    add_styled_heading(doc, "5. 示範數據生成與文件化 (Demo Seeding & Documentation)", level=2)
    add_body_paragraph(doc,
        "為使期中展示具備專業說服力，AI 協助編寫了 seed_demo_data.py，自動模擬當月份不同日期、多個帳戶與分類的收支數據，並故意製造一筆餐飲預算超支情境，方便口頭報告時直接向評審老師展示即時警報與視覺化效果。同時，完善了工程級的 README.md 與單元測試。"
    )

    # ==========================================================
    # 肆、查了什麼 (Research, Technical Selection & References)
    # ==========================================================
    add_styled_heading(doc, "肆、查了什麼 (技術調研、文獻探討與選型決策)", level=1)
    add_body_paragraph(doc, "在專案研發歷程中，團隊針對前端介面、資料庫引擎、圖表函式庫與軟體工程實踐進行了深度調研與權衡評估：")

    add_styled_heading(doc, "1. 前端框架選型評估：Streamlit vs. Tkinter vs. Flask/Vue", level=2)
    add_body_paragraph(doc,
        "• 桌面 GUI (Tkinter/PyQt)：跨平台打包容易出現字型模糊與樣式老舊，且缺乏現代化響應式排版，期中展示效果較受限。\n"
        "• 前後端分離 (Flask + Vue.js/React)：架構雖標準但工程負擔龐大，需維護大量 API 路由與前端狀態管理，在期中有限時程內難以兼顧深度功能與圖表美感。\n"
        "• Streamlit 框架（最終勝出）：專為數據科學與敏捷原型打造，具備 Python 原生代碼驅動、內建豐富佈局元件（如 st.metric、st.progress、st.tabs）、即時狀態重繪（Re-run）機制，能在最短時間內產出兼具現代質感與高度互動性的專業 Web 介面。"
    )

    add_styled_heading(doc, "2. 圖表引擎選型評估：Plotly vs. Matplotlib / Seaborn", level=2)
    add_body_paragraph(doc,
        "Matplotlib 生成的是靜態點陣圖片，無法動態懸停查看數值細節，且在中文字型顯示上常出現豆腐塊亂碼。經過技術查證，選用以 JavaScript 核心驅動的 Plotly 圖表庫。Plotly 不僅具備流暢的動畫與 Hover 資訊提示卡，還能將圖表完美嵌入 Streamlit 網頁中，呈現極佳的視覺美感。"
    )

    add_styled_heading(doc, "3. 資料存儲調研：SQLite 嵌入式關聯資料庫", level=2)
    add_body_paragraph(doc,
        "研讀 SQLite 官方文件與 ACID 特性，確認 SQLite 支援標準 SQL 語法、單檔案儲存特性且不依賴獨立的後台常駐行程（Serverless）。非常適合作為單機個人記帳應用的資料底層，利於打包、遷移與離線備份。"
    )

    add_styled_heading(doc, "4. 參考資源與技術文獻清單", level=2)
    add_bullet_item(doc, "Streamlit 官方文件：", "https://docs.streamlit.io/ (特別參考 Session State 管理、st.form 表單防抖動提交與自訂 CSS 注入機制)")
    add_bullet_item(doc, "Plotly Python API Reference：", "https://plotly.com/python/ (研究 Donut Charts 圓形挖空參數與 Grouped Bar Chart 雙軸設定)")
    add_bullet_item(doc, "SQLite3 官方技術規範：", "https://www.sqlite.org/foreignkeys.html (深入研讀 Foreign Key 參照完整性與 ON CONFLICT DO UPDATE upsert 語法)")
    add_bullet_item(doc, "Python 軟體工程實踐與單元測試：", "Python 內建 unittest 模組架構、contextmanager 資源生命週期管理最佳實踐")

    # ==========================================================
    # 伍、下一步 (Future Roadmap & Expansion)
    # ==========================================================
    add_styled_heading(doc, "伍、下一步 (未來展望與擴充規劃)", level=1)
    add_body_paragraph(doc, "SmartLedger 已經具備了堅實的資料庫結構與流暢的操作體驗，針對未來的期末專題或商業化發佈，規劃了以下四個擴充方向：")

    add_bullet_item(doc, "1. 整合生成式 AI 智慧記帳助理 (LLM Natural Language Expense Logging)：", "引進 Gemini API 或 OpenAI 介面，讓使用者可直接透過自然語言一句話記帳（例如：「剛剛在 7-11 悠遊卡刷了 120 元午餐」）。AI 自動解析交易時間、類型、金額、分類與扣款帳戶，實現極致便捷的零負擔記帳體驗。")
    add_bullet_item(doc, "2. 雲端化與多使用者權限隔離 (Cloud Deployment & Multi-User Auth)：", "目前系統為單機本地版，未來可整合 PostgreSQL 與 Streamlit Authenticator 帳號驗證套件，將應用無痛部署至 Streamlit Community Cloud 或 Render 雲端平台，支援使用者跨手機、電腦同步雲端記帳。")
    add_bullet_item(doc, "3. 發票載具與 OCR 拍照辨識自動記帳 (Receipt OCR)：", "利用電腦視覺 OCR 技術，支援拍照上傳紙本發票或收據，自動辨識消費品項、總金額與商店名稱並歸檔，進一步降低手動輸入的時間成本。")
    add_bullet_item(doc, "4. 週期性固定收支自動排程 (Recurring Transactions)：", "新增每月自動扣繳功能（如定期房租、水電瓦斯、Netflix/Spotify 訂閱費、每月定期定額存股等），在設定日期自動寫入交易紀錄並發出推播提醒。")

    # 結語
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    summary_box = doc.add_table(rows=1, cols=1)
    summary_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sum = summary_box.rows[0].cells[0]
    c_sum.width = Inches(6.5)
    set_cell_background(c_sum, "EBF5FB")
    set_cell_margins(c_sum, 120, 120, 160, 160)
    p_sum = c_sum.paragraphs[0]
    p_sum.paragraph_format.line_spacing = 1.25
    r_sum_title = p_sum.add_run("結語與自我省思：\n")
    format_run(r_sum_title, font_name="微軟正黑體", size_pt=11.5, bold=True, color_rgb=(26, 82, 118))
    r_sum_body = p_sum.add_run(
        "本次期中專案不僅成功研發出一款高度客製化、實用且視覺精美的智慧記帳工具，更關鍵的收穫在於親身體驗並驗證了「AI 結對協同開發（Human-AI Collaboration）」的高效潛力。透過人類把控業務方向與架構決策、AI 專注於敏捷原型建置與細節除錯，不僅大幅縮短了專案落地時程，更全面提升了軟體的工程規範度與代碼品質。"
    )
    format_run(r_sum_body, font_name="微軟正黑體", size_pt=10.5, color_rgb=(44, 62, 80))

    doc.save(output_filename)
    print(f"✅ Word 報告已成功生成至：{output_filename}")

if __name__ == "__main__":
    build_word_report()
