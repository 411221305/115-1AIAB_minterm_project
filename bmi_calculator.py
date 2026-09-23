"""
BMI Calculator (Body Mass Index) - Version 2.1
A command-line tool to calculate BMI, analyze health categories,
and suggest ideal weight ranges with multilingual support:
English, Traditional Chinese (繁體中文), Japanese (日本語), and Korean (한국어).
"""

import argparse
from typing import Callable, Tuple

MESSAGES = {
    "en": {
        "title": "Welcome to the BMI Calculator (v2.1)",
        "quit_hint": "Type 'q' or 'exit' anytime to quit.",
        "prompt_height": "Enter your height (in cm or meters, e.g. 175 or 1.75): ",
        "prompt_weight": "Enter your weight (in kg, e.g. 68.5): ",
        "prompt_again": "Would you like to calculate another? (Y/n): ",
        "goodbye": "Thank you for using BMI Calculator. Stay healthy!",
        "exit_msg": "\nExiting BMI Calculator. Goodbye!",
        "invalid_input": "Invalid input",
        "try_again": "Please try again (or enter 'q' to quit).",
        "err_height_positive": "Height must be greater than zero.",
        "err_weight_positive": "Weight must be greater than zero.",
        "err_height_range": "Height {val:.2f}m is outside plausible human range (0.5m - 2.8m).",
        "err_weight_range": "Weight {val:.1f}kg is outside plausible human range (10kg - 500kg).",
        "report_header": "BMI REPORT SUMMARY",
        "lbl_height": "Height",
        "lbl_weight": "Weight",
        "lbl_bmi": "BMI",
        "lbl_category": "Category",
        "lbl_ideal_weight": "Ideal Weight",
        "lbl_advice": "Health Advice",
        "cat_underweight": "Underweight",
        "cat_normal": "Normal Weight",
        "cat_overweight": "Overweight",
        "cat_mild_obesity": "Mild Obesity (Class I)",
        "cat_moderate_obesity": "Moderate Obesity (Class II)",
        "cat_severe_obesity": "Severe Obesity (Class III)",
        "adv_underweight": "Consider consulting a healthcare professional for balanced nutritional guidance.",
        "adv_normal": "Great job! Keep maintaining a balanced diet and regular physical activity.",
        "adv_overweight": "Pay attention to your dietary intake and increase moderate aerobic exercise.",
        "adv_mild_obesity": "Advisable to adjust diet, exercise regularly, and monitor health markers.",
        "adv_moderate_obesity": "Consult a physician or dietitian for a structured weight management plan.",
        "adv_severe_obesity": "Medical supervision and specialized health consultation are strongly recommended.",
    },
    "zh-tw": {
        "title": "歡迎使用 BMI 計算機 (v2.1)",
        "quit_hint": "隨時輸入 'q' 或 'exit' 即可退出程式。",
        "prompt_height": "請輸入您的身高（公分或公尺，例如 175 或 1.75）：",
        "prompt_weight": "請輸入您的體重（公斤，例如 68.5）：",
        "prompt_again": "是否要再計算一次？ (Y/n)：",
        "goodbye": "感謝使用 BMI 計算機，祝您健康！",
        "exit_msg": "\n已退出 BMI 計算機，再見！",
        "invalid_input": "輸入無效",
        "try_again": "請重新輸入（或輸入 'q' 退出）。",
        "err_height_positive": "身高必須大於零。",
        "err_weight_positive": "體重必須大於零。",
        "err_height_range": "身高 {val:.2f} 公尺超出合理人類範圍 (0.5m - 2.8m)。",
        "err_weight_range": "體重 {val:.1f} 公斤超出合理人類範圍 (10kg - 500kg)。",
        "report_header": "BMI 健康分析報告",
        "lbl_height": "身高",
        "lbl_weight": "體重",
        "lbl_bmi": "BMI 數值",
        "lbl_category": "體位狀態",
        "lbl_ideal_weight": "理想體重範圍",
        "lbl_advice": "健康建議",
        "cat_underweight": "體重過輕 (Underweight)",
        "cat_normal": "正常體位 (Normal Weight)",
        "cat_overweight": "過重 (Overweight)",
        "cat_mild_obesity": "輕度肥胖 (Mild Obesity)",
        "cat_moderate_obesity": "中度肥胖 (Moderate Obesity)",
        "cat_severe_obesity": "重度肥胖 (Severe Obesity)",
        "adv_underweight": "建議諮詢營養師或專業醫師，獲取均衡飲食指引以增補營養。",
        "adv_normal": "太棒了！請繼續維持良好的飲食習慣與規律的有氧/肌力運動。",
        "adv_overweight": "注意控制飲食熱量攝取，並適度增加每週中強度有氧運動。",
        "adv_mild_obesity": "建議積極調整生活與飲食習慣，定期追蹤血糖、血脂等健康指標。",
        "adv_moderate_obesity": "建議尋求醫師或營養專科團隊規劃個人化減重方案。",
        "adv_severe_obesity": "強烈建議接受專業醫療諮詢與減重門診全面評估。",
    },
    "ja": {
        "title": "BMI 計算機へようこそ (v2.1)",
        "quit_hint": "'q' または 'exit' を入力するといつでも終了できます。",
        "prompt_height": "身長を入力してください（cm または m、例: 175 または 1.75）: ",
        "prompt_weight": "体重を入力してください（kg、例: 68.5）: ",
        "prompt_again": "もう一度計算しますか？ (Y/n): ",
        "goodbye": "BMI 計算機をご利用いただきありがとうございました。健康にお過ごしください！",
        "exit_msg": "\nBMI 計算機を終了しました。さようなら！",
        "invalid_input": "無効な入力です",
        "try_again": "もう一度お試しください（終了する場合は 'q' を入力）。",
        "err_height_positive": "身長は 0 より大きい必要があります。",
        "err_weight_positive": "体重は 0 より大きい必要があります。",
        "err_height_range": "身長 {val:.2f}m は人間の標準的な範囲 (0.5m - 2.8m) 外です。",
        "err_weight_range": "体重 {val:.1f}kg は人間の標準的な範囲 (10kg - 500kg) 外です。",
        "report_header": "BMI 健康分析レポート",
        "lbl_height": "身長",
        "lbl_weight": "体重",
        "lbl_bmi": "BMI 数値",
        "lbl_category": "判定",
        "lbl_ideal_weight": "適正体重範囲",
        "lbl_advice": "健康アドバイス",
        "cat_underweight": "低体重・やせ型 (Underweight)",
        "cat_normal": "普通体重 (Normal Weight)",
        "cat_overweight": "肥満予備軍・過体重 (Overweight)",
        "cat_mild_obesity": "肥満（1度）",
        "cat_moderate_obesity": "肥満（2度）",
        "cat_severe_obesity": "肥満（3度以上・高度肥満）",
        "adv_underweight": "医師や管理栄養士に相談し、バランスの良い栄養摂取を心がけましょう。",
        "adv_normal": "素晴らしいです！現在のバランスの取れた食事と適度な運動を維持しましょう。",
        "adv_overweight": "食事のカロリー摂取量を見直し、有酸素運動を少しずつ増やしていきましょう。",
        "adv_mild_obesity": "生活習慣と食事を見直し、定期的に血圧や血糖値などを確認しましょう。",
        "adv_moderate_obesity": "医師や専門チームと相談し、計画的な体重管理プログラムを検討してください。",
        "adv_severe_obesity": "専門医による診察やメディカルダイエット指導を受けることを強く推奨します。",
    },
    "ko": {
        "title": "BMI 계산기에 오신 것을 환영합니다 (v2.1)",
        "quit_hint": "언제든지 'q' 또는 'exit'를 입력하여 종료할 수 있습니다.",
        "prompt_height": "키를 입력하세요 (cm 또는 m, 예: 175 또는 1.75): ",
        "prompt_weight": "몸무게를 입력하세요 (kg, 예: 68.5): ",
        "prompt_again": "다시 계산하시겠습니까? (Y/n): ",
        "goodbye": "BMI 계산기를 이용해 주셔서 감사합니다. 늘 건강하세요!",
        "exit_msg": "\nBMI 계산기를 종료합니다. 안녕히 가세요!",
        "invalid_input": "잘못된 입력입니다",
        "try_again": "다시 입력해 주세요 (종료하려면 'q' 입력).",
        "err_height_positive": "키는 0보다 커야 합니다.",
        "err_weight_positive": "몸무게는 0보다 커야 합니다.",
        "err_height_range": "키 {val:.2f}m는 일반적인 사람의 범위(0.5m ~ 2.8m)를 벗어났습니다.",
        "err_weight_range": "몸무게 {val:.1f}kg는 일반적인 사람의 범위(10kg ~ 500kg)를 벗어났습니다.",
        "report_header": "BMI 건강 분석 결과",
        "lbl_height": "신장(키)",
        "lbl_weight": "체중(몸무게)",
        "lbl_bmi": "BMI 수치",
        "lbl_category": "비만도 분류",
        "lbl_ideal_weight": "적정 체중 범위",
        "lbl_advice": "건강 권장사항",
        "cat_underweight": "저체중 (Underweight)",
        "cat_normal": "정상 체중 (Normal Weight)",
        "cat_overweight": "과체중 (Overweight)",
        "cat_mild_obesity": "경도 비만 (1단계)",
        "cat_moderate_obesity": "중등도 비만 (2단계)",
        "cat_severe_obesity": "고도 비만 (3단계)",
        "adv_underweight": "전문가와 상담하여 균형 잡힌 영양 섭취 계획을 세우는 것이 좋습니다.",
        "adv_normal": "훌륭합니다! 현재의 건강한 식습관과 규칙적인 운동을 꾸준히 유지하세요.",
        "adv_overweight": "식사량을 조절하고 유산소 운동 빈도를 점진적으로 늘려보세요.",
        "adv_mild_obesity": "생활 습관 및 식단을 개선하고 정기적으로 건강 상태를 점검하세요.",
        "adv_moderate_obesity": "의사 또는 영양 전문가의 도움을 받아 체계적인 체중 감량을 권장합니다.",
        "adv_severe_obesity": "전문 의료진의 진료 및 맞춤형 건강 관리 치료를 강력히 권장합니다.",
    },
}


def normalize_lang(lang: str) -> str:
    """Normalize language code to supported keys ('en', 'zh-tw', 'ja', 'ko')."""
    if not lang:
        return "en"
    lang_clean = lang.lower().strip().replace("_", "-")
    if lang_clean in ("zh", "zh-tw", "zh-hant", "tw", "2"):
        return "zh-tw"
    if lang_clean in ("ja", "jp", "japanese", "3"):
        return "ja"
    if lang_clean in ("ko", "kr", "korean", "4"):
        return "ko"
    return "en"


def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """Retrieve localized message string with fallback to English."""
    lang_key = normalize_lang(lang)
    tmpl = MESSAGES.get(lang_key, MESSAGES["en"]).get(key, MESSAGES["en"].get(key, key))
    if kwargs:
        return tmpl.format(**kwargs)
    return tmpl


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index (BMI).
    
    Formula: weight (kg) / [height (m)]^2
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    return round(weight_kg / (height_m ** 2), 2)


def get_bmi_category(bmi: float, lang: str = "en") -> Tuple[str, str]:
    """Return localized health category and advice based on standard health guidelines."""
    lang_key = normalize_lang(lang)
    if bmi < 18.5:
        category = get_text("cat_underweight", lang_key)
        advice = get_text("adv_underweight", lang_key)
    elif 18.5 <= bmi < 24.0:
        category = get_text("cat_normal", lang_key)
        advice = get_text("adv_normal", lang_key)
    elif 24.0 <= bmi < 27.0:
        category = get_text("cat_overweight", lang_key)
        advice = get_text("adv_overweight", lang_key)
    elif 27.0 <= bmi < 30.0:
        category = get_text("cat_mild_obesity", lang_key)
        advice = get_text("adv_mild_obesity", lang_key)
    elif 30.0 <= bmi < 35.0:
        category = get_text("cat_moderate_obesity", lang_key)
        advice = get_text("adv_moderate_obesity", lang_key)
    else:
        category = get_text("cat_severe_obesity", lang_key)
        advice = get_text("adv_severe_obesity", lang_key)
    
    return category, advice


def get_ideal_weight_range(height_m: float) -> Tuple[float, float]:
    """Calculate ideal healthy weight range (BMI 18.5 to 24.0) for a given height."""
    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.0 * (height_m ** 2), 1)
    return min_weight, max_weight


def parse_height(raw_input: str, lang: str = "en") -> float:
    """Parse height input, supporting meters (e.g. 1.75) or centimeters (e.g. 175)."""
    lang_key = normalize_lang(lang)
    val = float(raw_input.strip())
    if val <= 0:
        raise ValueError(get_text("err_height_positive", lang_key))
    if val > 3.0:
        val = val / 100.0
    if val < 0.5 or val > 2.8:
        raise ValueError(get_text("err_height_range", lang_key, val=val))
    return val


def parse_weight(raw_input: str, lang: str = "en") -> float:
    """Parse weight input in kilograms."""
    lang_key = normalize_lang(lang)
    val = float(raw_input.strip())
    if val <= 0:
        raise ValueError(get_text("err_weight_positive", lang_key))
    if val < 10.0 or val > 500.0:
        raise ValueError(get_text("err_weight_range", lang_key, val=val))
    return val


def display_report(height_m: float, weight_kg: float, bmi: float, lang: str = "en") -> None:
    """Format and print localized BMI summary report."""
    lang_key = normalize_lang(lang)
    category, advice = get_bmi_category(bmi, lang_key)
    ideal_min, ideal_max = get_ideal_weight_range(height_m)
    
    title = get_text("report_header", lang_key)
    lbl_h = get_text("lbl_height", lang_key)
    lbl_w = get_text("lbl_weight", lang_key)
    lbl_b = get_text("lbl_bmi", lang_key)
    lbl_c = get_text("lbl_category", lang_key)
    lbl_i = get_text("lbl_ideal_weight", lang_key)
    lbl_a = get_text("lbl_advice", lang_key)
    
    print("\n" + "=" * 54)
    print(f"               {title.center(24)}               ")
    print("=" * 54)
    print(f" {lbl_h:<16}: {height_m * 100:.1f} cm ({height_m:.2f} m)")
    print(f" {lbl_w:<16}: {weight_kg:.1f} kg")
    print(f" {lbl_b:<16}: {bmi:.2f}")
    print(f" {lbl_c:<16}: {category}")
    print(f" {lbl_i:<16}: {ideal_min} kg ~ {ideal_max} kg")
    print("-" * 54)
    print(f" {lbl_a:<16}: {advice}")
    print("=" * 54 + "\n")


def prompt_input(prompt_text: str, parser_func: Callable[[str], float], lang: str) -> float:
    """Repeatedly prompt user until valid input is received or user exits."""
    lang_key = normalize_lang(lang)
    while True:
        user_val = input(prompt_text).strip()
        if user_val.lower() in ("q", "quit", "exit"):
            raise KeyboardInterrupt
        try:
            return parser_func(user_val)
        except ValueError as err:
            err_title = get_text("invalid_input", lang_key)
            try_again = get_text("try_again", lang_key)
            print(f" [!] {err_title}: {err} {try_again}")


def choose_language_interactively() -> str:
    """Prompt user to choose language when not supplied via CLI argument."""
    print("=" * 54)
    print("  Language Selection / 語言選擇 / 言語選択 / 언어 선택")
    print("  1. English (Default)")
    print("  2. 繁體中文 (Traditional Chinese - zh-tw)")
    print("  3. 日本語 (Japanese - ja)")
    print("  4. 한국어 (Korean - ko)")
    print("=" * 54)
    choice = input("Please select [1/2/3/4] (預設為 1): ").strip()
    return normalize_lang(choice)


def main() -> None:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Multilingual BMI Calculator (en, zh-tw, ja, ko)")
    parser.add_argument(
        "--lang",
        choices=["en", "zh-tw", "zh", "ja", "ko"],
        default=None,
        help="UI Language (en, zh-tw, ja, ko)",
    )
    args = parser.parse_args()

    if args.lang:
        lang = normalize_lang(args.lang)
    else:
        lang = choose_language_interactively()

    print("\n" + "=" * 54)
    print(f"   {get_text('title', lang)}   ")
    print("=" * 54)
    print(f"{get_text('quit_hint', lang)}\n")

    while True:
        try:
            height = prompt_input(get_text("prompt_height", lang), lambda val: parse_height(val, lang), lang)
            weight = prompt_input(get_text("prompt_weight", lang), lambda val: parse_weight(val, lang), lang)
            
            bmi = calculate_bmi(weight, height)
            display_report(height, weight, bmi, lang)

            again = input(get_text("prompt_again", lang)).strip().lower()
            if again in ("n", "no", "q", "quit", "exit", "否", "いいえ", "아니오"):
                print(get_text("goodbye", lang))
                break
            print()
        except (KeyboardInterrupt, EOFError):
            print(get_text("exit_msg", lang))
            break


if __name__ == "__main__":
    main()
