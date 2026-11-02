# -*- coding: utf-8 -*-
"""
generate_slides.py
產生期中專案班級口頭發表簡報投影片 (.pptx)
專為 16:9 寬螢幕設計，具備現代專業科技風配色與視覺化資訊卡片排版。
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# 配色常數定義 (科技藍與典雅灰白)
NAVY_DARK = RGBColor(20, 40, 65)        # 標題深海軍藍 #142841
PRIMARY_BLUE = RGBColor(31, 110, 165)   # 核心藍色 #1F6EA5
ACCENT_CYAN = RGBColor(41, 171, 226)    # 亮天藍 #29ABE2
ACCENT_CORAL = RGBColor(235, 87, 87)    # 警戒紅 #EB5757
ACCENT_GREEN = RGBColor(46, 204, 113)   # 成功綠 #2ECC71
BG_LIGHT = RGBColor(248, 250, 252)      # 淺灰底色 #F8FAFC
CARD_BG = RGBColor(255, 255, 255)       # 卡片純白
TEXT_MAIN = RGBColor(40, 50, 60)        # 主文字 #28323C
TEXT_MUTED = RGBColor(110, 120, 135)    # 次要文字 #6E7887
BORDER_COLOR = RGBColor(220, 228, 235)  # 邊框灰

def set_font(run, text=None, font_name="微軟正黑體", size_pt=14, bold=False, color=TEXT_MAIN):
    if text is not None:
        run.text = text
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.font.color.rgb = color

def create_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    """建立圓角卡片底塊"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def add_header(slide, title_text, category_text="SmartLedger 期中專題發表"):
    """每頁標準頂部標題列"""
    # 頂部裝飾細線
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_CYAN
    line.line.fill.background()

    # 次標題 / 分類標籤
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(10), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    r_c = p_c.add_run()
    set_font(r_c, text=category_text.upper(), size_pt=10, bold=True, color=PRIMARY_BLUE)

    # 主標題
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    r_t = p_t.add_run()
    set_font(r_t, text=title_text, size_pt=24, bold=True, color=NAVY_DARK)

def build_presentation(filename="SmartLedger_專案介紹簡報.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # Slide 1: 封面頁 (Title Slide)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    dec1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(1.2), Inches(1.8), Inches(0.4))
    dec1.fill.solid()
    dec1.fill.fore_color.rgb = PRIMARY_BLUE
    dec1.line.fill.background()
    p_d = dec1.text_frame.paragraphs[0]
    p_d.alignment = PP_ALIGN.CENTER
    r_d = p_d.add_run()
    set_font(r_d, text="115-1 期中專案成果", size_pt=11, bold=True, color=RGBColor(255, 255, 255))

    tb_title = s1.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(11.5), Inches(3.2))
    tf1 = tb_title.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    r1 = p1.add_run()
    set_font(r1, text="SmartLedger", size_pt=48, bold=True, color=RGBColor(255, 255, 255))
    
    p2 = tf1.add_paragraph()
    p2.space_before = Pt(8)
    r2 = p2.add_run()
    set_font(r2, text="客製化智慧記帳與三段式預算監控系統", size_pt=26, bold=True, color=ACCENT_CYAN)

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(14)
    r3 = p3.add_run()
    set_font(r3, text="告別固定死板分類！打造真正貼合個人生活與多元支付通路的財務儀表板", size_pt=14, color=RGBColor(200, 215, 230))

    info_box = s1.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.333), Inches(1.2))
    tf_info = info_box.text_frame
    p_i = tf_info.paragraphs[0]
    r_i = p_i.add_run()
    set_font(r_i, text="報告人：專案團隊　｜　核心架構：Python + Streamlit + SQLite + Plotly　｜　開發模式：人機協同 (AI Pair Programming)", size_pt=12, color=RGBColor(160, 180, 205))

    # =========================================================================
    # Slide 2: 為什麼要做這個？傳統記帳三大痛點 (Problem Statement)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "為什麼要做這個？痛點與發想初衷", "Background & Motivation")

    pain_points = [
        ("❌ 分類固定死板，難以客製", "市面 App 項目僵化，像大學生常買手搖飲、社團聚餐、動漫周邊，只能塞進「其他」，最後根本看不出錢花在哪。"),
        ("❌ 忽略無現金支付多通路", "現代人皮夾有現金，手機有 Line Pay、街口、悠遊卡跟信用卡。傳統記帳只記單純數字，卡片到底剩多少錢完全不知道！"),
        ("❌ 被動記帳，月底才知吃土", "記帳通常是「事後記錄」，缺乏主動預算警戒機制。往往到了月底戶頭歸零，才驚覺某個分類早就嚴重透支！")
    ]

    card_w = Inches(3.64)
    card_h = Inches(4.8)
    for i, (title, desc) in enumerate(pain_points):
        left = Inches(0.8 + i * 4.0)
        create_card(s2, left, Inches(1.8), card_w, card_h)
        
        strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), card_w, Inches(0.9))
        strip.fill.solid()
        strip.fill.fore_color.rgb = RGBColor(253, 237, 236)
        strip.line.fill.background()
        p_st = strip.text_frame.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        r_st = p_st.add_run()
        set_font(r_st, text=title, size_pt=13, bold=True, color=ACCENT_CORAL)

        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(2.9), card_w - Inches(0.4), card_h - Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.line_spacing = 1.3
        r = p.add_run()
        set_font(r, text=desc, size_pt=13, color=TEXT_MAIN)

    # =========================================================================
    # Slide 3: SmartLedger 解法：三大核心特色 (Core Features)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "SmartLedger 核心解法：高彈性、主動警示、視覺化", "Solution & Value Proposition")

    features = [
        ("🎨 100% 自由自訂義", "自訂收支分類 + 自選 Emoji", "可自由擴充類別並配上可愛 Emoji（🍔 美食、🚌 通勤、🎁 獎金）。支援獨立現金、Line Pay、悠遊卡、銀行帳戶餘額動態計算！"),
        ("🚨 三段式主動超支警報", "綠色安全 ➔ 黃色警戒 ➔ 紅色超支", "為分類設定月預算。花費達 80% 自動跳出黃色警訊；超過 100% 首頁立刻彈出全域紅色警報，精準算出超支多少！"),
        ("📊 Plotly 互動視覺化", "分類環形圖 + 每日收支走勢圖", "滑鼠懸停即可探索每一筆開銷佔比；即時計算當月總收入、總支出與淨結餘，一秒看懂自身資產健康度！")
    ]

    for i, (tag, subtitle, desc) in enumerate(features):
        left = Inches(0.8 + i * 4.0)
        create_card(s3, left, Inches(1.8), card_w, card_h)
        
        strip = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), card_w, Inches(0.9))
        strip.fill.solid()
        strip.fill.fore_color.rgb = RGBColor(235, 245, 251)
        strip.line.fill.background()
        p_st = strip.text_frame.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        r_st = p_st.add_run()
        set_font(r_st, text=tag, size_pt=13, bold=True, color=PRIMARY_BLUE)

        tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(2.9), card_w - Inches(0.4), card_h - Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_sub = tf.paragraphs[0]
        r_sub = p_sub.add_run()
        set_font(r_sub, text=subtitle + "\n\n", size_pt=12, bold=True, color=NAVY_DARK)

        p = tf.add_paragraph()
        p.line_spacing = 1.3
        r = p.add_run()
        set_font(r, text=desc, size_pt=12, color=TEXT_MAIN)

    # =========================================================================
    # Slide 4: 系統架構與技術棧 (Architecture & Tech Stack)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "嚴謹的模組化架構與技術選型", "System Architecture & Engineering")

    create_card(s4, Inches(0.8), Inches(1.8), Inches(7.2), Inches(4.8))
    tb_arch = s4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(6.6), Inches(4.4))
    tf_a = tb_arch.text_frame
    tf_a.word_wrap = True
    
    arch_steps = [
        ("🖥️ 展示層 (Presentation Layer) - app.py", "採用 Streamlit 構建直觀網頁前端，具備側邊欄分頁導航、響應式表單防呆提交與全域月份切換器。"),
        ("📈 視覺化層 (Visualization Layer) - charts.py", "透過 Plotly 繪製 Donut 環形佔比圖、每日收支對比柱狀圖與預算進度長條圖，支援零資料防崩潰機制。"),
        ("⚙️ 商業邏輯層 (Business Logic) - services.py", "處理交易 CRUD、帳戶資產動態計算、三色警戒狀態判定演算法與 UTF-8 BOM CSV 匯出匯入。"),
        ("🗄️ 資料持久層 (Database Layer) - database.py", "SQLite3 輕量嵌入式資料庫，嚴格啟用外鍵參照約束 (PRAGMA foreign_keys = ON) 與種子資料冷啟動機制。")
    ]
    for idx, (title, desc) in enumerate(arch_steps):
        p_t = tf_a.paragraphs[0] if idx == 0 else tf_a.add_paragraph()
        if idx > 0:
            p_t.space_before = Pt(8)
        r_t = p_t.add_run()
        set_font(r_t, text=title + "\n", size_pt=12, bold=True, color=PRIMARY_BLUE)
        r_d = p_t.add_run()
        set_font(r_d, text=desc, size_pt=10.5, color=TEXT_MAIN)

    create_card(s4, Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.8))
    tb_tech = s4.shapes.add_textbox(Inches(8.5), Inches(2.0), Inches(3.8), Inches(4.4))
    tf_tech = tb_tech.text_frame
    tf_tech.word_wrap = True

    p_th = tf_tech.paragraphs[0]
    r_th = p_th.add_run()
    set_font(r_th, text="🛠️ 核心技術清單\n\n", size_pt=14, bold=True, color=NAVY_DARK)

    tech_list = [
        ("Python 3.13", "現代語法與型別標註"),
        ("Streamlit 1.66", "數據驅動極速 Web 構建"),
        ("SQLite 3", "免伺服器、單檔持久化儲存"),
        ("Plotly 7.1", "互動式專業動態圖表"),
        ("Pandas 3.1", "高效結構化資料過濾與分析"),
        ("Unittest", "自動化測試套件 (4/4 綠燈通過)")
    ]
    for name, note in tech_list:
        p = tf_tech.add_paragraph()
        p.space_before = Pt(4)
        r_n = p.add_run()
        set_font(r_n, text=f"• {name}：", size_pt=11, bold=True, color=PRIMARY_BLUE)
        r_o = p.add_run()
        set_font(r_o, text=note, size_pt=10.5, color=TEXT_MAIN)

    # =========================================================
    # Slide 5: 人機協同開發工作流 (Human-AI Collaboration)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "我們是怎麼跟 AI 一起完成這個專案的？", "Human-AI Pair Programming Workflow")

    collab_stages = [
        ("1. 需求訪談與藍圖", "人類擔任 PM/架構師，提出自訂義與預算痛點；AI 梳理 Streamlit vs PyQt 選型並制定 6 階段開發 Roadmap。"),
        ("2. 資料庫規範化", "共同擬定 categories、accounts、records、budgets 四大關聯表，AI 編寫 Schema DDL 與預設種子資料。"),
        ("3. 實作與防呆驗證", "AI 快速產生模組化代碼；實作帳戶防誤刪檢核、金額正數防呆與圖表空資料保護機制。"),
        ("4. 協同排錯與突破", "遭遇 Windows 檔案鎖死報錯 (WinError 32)；AI 迅速以 contextmanager 與 gc 重構連線管理，單元測試滿分通過！")
    ]

    card_w4 = Inches(2.7)
    for i, (stage_title, stage_desc) in enumerate(collab_stages):
        left = Inches(0.8 + i * 3.0)
        create_card(s5, left, Inches(1.8), card_w4, Inches(4.8))

        num_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), card_w4, Inches(0.8))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = PRIMARY_BLUE
        num_box.line.fill.background()
        p_nb = num_box.text_frame.paragraphs[0]
        p_nb.alignment = PP_ALIGN.CENTER
        r_nb = p_nb.add_run()
        set_font(r_nb, text=stage_title, size_pt=12, bold=True, color=RGBColor(255, 255, 255))

        tb_desc = s5.shapes.add_textbox(left + Inches(0.15), Inches(2.8), card_w4 - Inches(0.3), Inches(3.6))
        tf_desc = tb_desc.text_frame
        tf_desc.word_wrap = True
        p_d = tf_desc.paragraphs[0]
        p_d.line_spacing = 1.3
        r_d = p_d.add_run()
        set_font(r_d, text=stage_desc, size_pt=11, color=TEXT_MAIN)

    # =========================================================
    # Slide 6: 現場 Demo 導覽路徑 (Live Demo Highlights)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "現場 Demo 體驗路徑與展示亮點", "Live Demo Walkthrough")

    demo_steps = [
        ("Step 1：財務儀表板總覽", "展示當月總收支、淨結餘、總資產；點出最上方的「🚨 預算超支警示橫幅」，立刻吸引全場目光！"),
        ("Step 2：快速記下一筆外食開銷", "切換到「✍️ 快速記帳」，示範輸入 150 元午餐拉麵，選擇「現金錢包」扣款，看到氣球動畫與即時扣除餘額。"),
        ("Step 3：體驗極高自由度的自訂義", "到「⚙️ 自訂分類與帳戶」，即時新增一個「🧋 手搖手作」分類與「悠遊卡」帳戶，驗證完全客製化能力！"),
        ("Step 4：預算警示與 CSV 一鍵備份", "在「🎯 預算設定」查看進度條，最後到「💾 資料匯出」一鍵下載 CSV，展示能直接用 Excel 離線分析。")
    ]

    card_h2 = Inches(2.2)
    card_w2 = Inches(5.6)
    coords = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3))
    ]
    for i, (title, desc) in enumerate(demo_steps):
        l, t = coords[i]
        create_card(s6, l, t, card_w2, card_h2)
        
        tb = s6.shapes.add_textbox(l + Inches(0.25), t + Inches(0.2), card_w2 - Inches(0.5), card_h2 - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_title = tf.paragraphs[0]
        r_title = p_title.add_run()
        set_font(r_title, text=title + "\n", size_pt=13, bold=True, color=PRIMARY_BLUE)

        p_desc = tf.add_paragraph()
        p_desc.space_before = Pt(6)
        p_desc.line_spacing = 1.25
        r_desc = p_desc.add_run()
        set_font(r_desc, text=desc, size_pt=11.5, color=TEXT_MAIN)

    # =========================================================
    # Slide 7: 未來展望與下一步 (Future Roadmap)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "專案的下一步：邁向期末與商業化擴充", "Next Steps & Future Roadmap")

    next_features = [
        ("🤖 LLM 自然語言記帳", "串接 Gemini API", "使用者只需輸入或說出「剛剛在超商用悠遊卡買了 95 元便當」，AI 自動提取時間、項目、金額並完成歸檔！"),
        ("☁️ 雲端化與多使用者", "PostgreSQL + Auth 登入", "升級為多租戶雲端資料庫，支援帳號註冊登入，讓大家在手機與電腦間無縫同步自己的帳本。"),
        ("📸 發票與收據 OCR 辨識", "電腦視覺自動掃描", "拍照紙本發票或上傳電子發票載具，自動辨識消費品項與金額，實現完全零手動輸入。"),
        ("⏰ 週期性自動記帳排程", "每月固定收支自動扣款", "針對每月固定房租、電信費、Netflix 或 Spotify 訂閱制自動排程記帳，不再漏記固定支出。")
    ]

    for i, (title, tag, desc) in enumerate(next_features):
        left = Inches(0.8 + i * 3.0)
        create_card(s7, left, Inches(1.8), card_w4, Inches(4.8))

        strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.8), card_w4, Inches(0.85))
        strip.fill.solid()
        strip.fill.fore_color.rgb = RGBColor(235, 245, 251)
        strip.line.fill.background()
        p_st = strip.text_frame.paragraphs[0]
        p_st.alignment = PP_ALIGN.CENTER
        r_st = p_st.add_run()
        set_font(r_st, text=title, size_pt=12, bold=True, color=PRIMARY_BLUE)

        tb = s7.shapes.add_textbox(left + Inches(0.15), Inches(2.8), card_w4 - Inches(0.3), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_tag = tf.paragraphs[0]
        r_tag = p_tag.add_run()
        set_font(r_tag, text=tag + "\n\n", size_pt=11, bold=True, color=NAVY_DARK)

        p = tf.add_paragraph()
        p.line_spacing = 1.3
        r = p.add_run()
        set_font(r, text=desc, size_pt=11, color=TEXT_MAIN)

    # =========================================================
    # Slide 8: 結尾致謝與 Q&A 頁 (Conclusion & QA)
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = NAVY_DARK
    bg8.line.fill.background()

    tb_end = s8.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(3.8))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    p_e1 = tf_end.paragraphs[0]
    p_e1.alignment = PP_ALIGN.CENTER
    r_e1 = p_e1.add_run()
    set_font(r_e1, text="感謝聆聽，敬請指教！", size_pt=42, bold=True, color=RGBColor(255, 255, 255))

    p_e2 = tf_end.add_paragraph()
    p_e2.space_before = Pt(16)
    p_e2.alignment = PP_ALIGN.CENTER
    r_e2 = p_e2.add_run()
    set_font(r_e2, text="Q & A  歡迎交流提問\n", size_pt=24, bold=True, color=ACCENT_CYAN)

    p_e3 = tf_end.add_paragraph()
    p_e3.space_before = Pt(20)
    p_e3.alignment = PP_ALIGN.CENTER
    r_e3 = p_e3.add_run()
    set_font(r_e3, text="GitHub 專案完整代碼已開源：\nhttps://github.com/411221305/115-1AIAB_minterm_project", size_pt=14, color=RGBColor(200, 220, 240))

    prs.save(filename)
    print(f"✅ 簡報投影片已成功生成至：{filename}")

if __name__ == "__main__":
    build_presentation()
