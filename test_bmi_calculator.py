import unittest
from bmi_calculator import (
    calculate_bmi,
    get_bmi_category,
    get_ideal_weight_range,
    get_text,
    normalize_lang,
    parse_height,
    parse_weight,
)


class TestBMICalculatorMultilingual(unittest.TestCase):
    def test_calculate_bmi(self):
        self.assertEqual(calculate_bmi(70, 1.75), 22.86)
        self.assertEqual(calculate_bmi(50, 1.60), 19.53)

    def test_calculate_bmi_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_bmi(-5, 1.75)
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)

    def test_normalize_lang(self):
        self.assertEqual(normalize_lang("en"), "en")
        self.assertEqual(normalize_lang("EN"), "en")
        self.assertEqual(normalize_lang("zh-tw"), "zh-tw")
        self.assertEqual(normalize_lang("zh_TW"), "zh-tw")
        self.assertEqual(normalize_lang("zh"), "zh-tw")
        self.assertEqual(normalize_lang("2"), "zh-tw")
        self.assertEqual(normalize_lang("ja"), "ja")
        self.assertEqual(normalize_lang("jp"), "ja")
        self.assertEqual(normalize_lang("3"), "ja")
        self.assertEqual(normalize_lang("ko"), "ko")
        self.assertEqual(normalize_lang("kr"), "ko")
        self.assertEqual(normalize_lang("4"), "ko")
        self.assertEqual(normalize_lang("unknown"), "en")

    def test_get_bmi_category_en(self):
        cat, adv = get_bmi_category(17.0, "en")
        self.assertEqual(cat, "Underweight")
        self.assertTrue(adv.startswith("Consider"))

        cat, _ = get_bmi_category(22.0, "en")
        self.assertEqual(cat, "Normal Weight")

    def test_get_bmi_category_zh_tw(self):
        cat, adv = get_bmi_category(17.0, "zh-tw")
        self.assertIn("體重過輕", cat)
        self.assertIn("建議諮詢營養師", adv)

        cat, _ = get_bmi_category(22.0, "zh-tw")
        self.assertIn("正常體位", cat)

    def test_get_bmi_category_ja(self):
        cat, adv = get_bmi_category(17.0, "ja")
        self.assertIn("低体重", cat)
        self.assertIn("医師や管理栄養士に相談", adv)

        cat, _ = get_bmi_category(22.0, "ja")
        self.assertIn("普通体重", cat)

        cat, _ = get_bmi_category(28.0, "ja")
        self.assertIn("肥満（1度）", cat)

    def test_get_bmi_category_ko(self):
        cat, adv = get_bmi_category(17.0, "ko")
        self.assertIn("저체중", cat)
        self.assertIn("전문가와 상담", adv)

        cat, _ = get_bmi_category(22.0, "ko")
        self.assertIn("정상 체중", cat)

        cat, _ = get_bmi_category(31.0, "ko")
        self.assertIn("중등도 비만", cat)

    def test_get_ideal_weight_range(self):
        min_w, max_w = get_ideal_weight_range(1.80)
        self.assertEqual(min_w, 59.9)
        self.assertEqual(max_w, 77.8)

    def test_parse_height(self):
        self.assertAlmostEqual(parse_height("1.75", "en"), 1.75)
        self.assertAlmostEqual(parse_height("175", "ja"), 1.75)
        self.assertAlmostEqual(parse_height("175", "ko"), 1.75)

        with self.assertRaises(ValueError) as ctx:
            parse_height("-10", "ja")
        self.assertIn("0 より大きい", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            parse_height("0.3", "ko")
        self.assertIn("벗어났습니다", str(ctx.exception))

    def test_parse_weight(self):
        self.assertAlmostEqual(parse_weight("68.5", "ja"), 68.5)
        self.assertAlmostEqual(parse_weight("  75 ", "ko"), 75.0)

        with self.assertRaises(ValueError) as ctx:
            parse_weight("-5", "ko")
        self.assertIn("0보다 커야 합니다", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            parse_weight("600", "ja")
        self.assertIn("人間の標準的な範囲", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
