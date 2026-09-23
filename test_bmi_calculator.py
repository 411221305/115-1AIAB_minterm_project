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


class TestBMICalculatorV2(unittest.TestCase):
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
        self.assertEqual(normalize_lang("unknown"), "en")

    def test_get_bmi_category_en(self):
        cat, adv = get_bmi_category(17.0, "en")
        self.assertEqual(cat, "Underweight")
        self.assertTrue(adv.startswith("Consider"))

        cat, _ = get_bmi_category(22.0, "en")
        self.assertEqual(cat, "Normal Weight")

        cat, _ = get_bmi_category(25.5, "en")
        self.assertEqual(cat, "Overweight")

        cat, _ = get_bmi_category(28.0, "en")
        self.assertEqual(cat, "Mild Obesity (Class I)")

        cat, _ = get_bmi_category(32.0, "en")
        self.assertEqual(cat, "Moderate Obesity (Class II)")

        cat, _ = get_bmi_category(36.0, "en")
        self.assertEqual(cat, "Severe Obesity (Class III)")

    def test_get_bmi_category_zh_tw(self):
        cat, adv = get_bmi_category(17.0, "zh-tw")
        self.assertIn("體重過輕", cat)
        self.assertIn("建議諮詢營養師", adv)

        cat, _ = get_bmi_category(22.0, "zh-tw")
        self.assertIn("正常體位", cat)

        cat, _ = get_bmi_category(25.5, "zh-tw")
        self.assertIn("過重", cat)

        cat, _ = get_bmi_category(28.0, "zh-tw")
        self.assertIn("輕度肥胖", cat)

        cat, _ = get_bmi_category(32.0, "zh-tw")
        self.assertIn("中度肥胖", cat)

        cat, _ = get_bmi_category(36.0, "zh-tw")
        self.assertIn("重度肥胖", cat)

    def test_get_ideal_weight_range(self):
        min_w, max_w = get_ideal_weight_range(1.80)
        self.assertEqual(min_w, 59.9)
        self.assertEqual(max_w, 77.8)

    def test_parse_height(self):
        self.assertAlmostEqual(parse_height("1.75", "en"), 1.75)
        self.assertAlmostEqual(parse_height("175", "zh-tw"), 1.75)

        with self.assertRaises(ValueError) as ctx:
            parse_height("-10", "zh-tw")
        self.assertIn("身高必須大於零", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            parse_height("0.3", "en")
        self.assertIn("outside plausible human range", str(ctx.exception))

    def test_parse_weight(self):
        self.assertAlmostEqual(parse_weight("68.5", "en"), 68.5)
        self.assertAlmostEqual(parse_weight("  75 ", "zh-tw"), 75.0)

        with self.assertRaises(ValueError) as ctx:
            parse_weight("-5", "zh-tw")
        self.assertIn("體重必須大於零", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            parse_weight("600", "en")
        self.assertIn("outside plausible human range", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
