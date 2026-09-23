import unittest
from bmi_calculator import (
    calculate_bmi,
    get_bmi_category,
    get_ideal_weight_range,
    parse_height,
    parse_weight,
)


class TestBMICalculator(unittest.TestCase):
    def test_calculate_bmi(self):
        # 70 kg, 1.75 m -> 70 / (1.75^2) = 22.857... -> 22.86
        self.assertEqual(calculate_bmi(70, 1.75), 22.86)
        # 50 kg, 1.60 m -> 50 / (1.60^2) = 19.53
        self.assertEqual(calculate_bmi(50, 1.60), 19.53)

    def test_calculate_bmi_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_bmi(-5, 1.75)
        with self.assertRaises(ValueError):
            calculate_bmi(70, 0)
        with self.assertRaises(ValueError):
            calculate_bmi(70, -1.75)

    def test_get_bmi_category(self):
        cat, _ = get_bmi_category(17.0)
        self.assertIn("Underweight", cat)

        cat, _ = get_bmi_category(22.0)
        self.assertIn("Normal", cat)

        cat, _ = get_bmi_category(25.5)
        self.assertIn("Overweight", cat)

        cat, _ = get_bmi_category(28.0)
        self.assertIn("Mild Obesity", cat)

        cat, _ = get_bmi_category(32.0)
        self.assertIn("Moderate Obesity", cat)

        cat, _ = get_bmi_category(36.0)
        self.assertIn("Severe Obesity", cat)

    def test_get_ideal_weight_range(self):
        min_w, max_w = get_ideal_weight_range(1.80)
        # 18.5 * 1.8^2 = 59.94 -> 59.9
        # 24.0 * 1.8^2 = 77.76 -> 77.8
        self.assertEqual(min_w, 59.9)
        self.assertEqual(max_w, 77.8)

    def test_parse_height(self):
        # Meters
        self.assertAlmostEqual(parse_height("1.75"), 1.75)
        # Centimeters conversion
        self.assertAlmostEqual(parse_height("175"), 1.75)
        self.assertAlmostEqual(parse_height("  180  "), 1.80)

        # Invalid heights
        with self.assertRaises(ValueError):
            parse_height("-10")
        with self.assertRaises(ValueError):
            parse_height("0.3")  # too short
        with self.assertRaises(ValueError):
            parse_height("350")  # 3.5m too tall
        with self.assertRaises(ValueError):
            parse_height("abc")

    def test_parse_weight(self):
        self.assertAlmostEqual(parse_weight("68.5"), 68.5)
        self.assertAlmostEqual(parse_weight("  75 "), 75.0)

        with self.assertRaises(ValueError):
            parse_weight("5")  # below 10kg
        with self.assertRaises(ValueError):
            parse_weight("600")  # above 500kg
        with self.assertRaises(ValueError):
            parse_weight("xyz")


if __name__ == "__main__":
    unittest.main()
