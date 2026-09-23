"""
BMI Calculator (Body Mass Index)
A command-line tool to calculate BMI, analyze health category,
and suggest ideal weight ranges.
"""

from typing import Tuple


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index (BMI).
    
    Formula: weight (kg) / [height (m)]^2
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    
    return round(weight_kg / (height_m ** 2), 2)


def get_bmi_category(bmi: float) -> Tuple[str, str]:
    """Return health category and advice based on WHO and Taiwan MOHW guidelines."""
    if bmi < 18.5:
        category = "Underweight (體重過輕)"
        advice = "Consider consulting a healthcare professional for balanced nutritional guidance."
    elif 18.5 <= bmi < 24.0:
        category = "Normal Weight (健康體位 - 正常)"
        advice = "Great job! Keep maintaining a balanced diet and regular physical activity."
    elif 24.0 <= bmi < 27.0:
        category = "Overweight (過重)"
        advice = "Pay attention to your dietary intake and increase moderate aerobic exercise."
    elif 27.0 <= bmi < 30.0:
        category = "Mild Obesity (輕度肥胖)"
        advice = "Advisable to adjust diet, exercise regularly, and monitor health markers."
    elif 30.0 <= bmi < 35.0:
        category = "Moderate Obesity (中度肥胖)"
        advice = "Consult a physician or dietitian for a structured weight management plan."
    else:
        category = "Severe Obesity (重度肥胖)"
        advice = "Medical supervision and specialized health consultation are strongly recommended."
    
    return category, advice


def get_ideal_weight_range(height_m: float) -> Tuple[float, float]:
    """Calculate the ideal healthy weight range (BMI 18.5 to 24.0) for a given height."""
    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.0 * (height_m ** 2), 1)
    return min_weight, max_weight


def parse_height(raw_input: str) -> float:
    """Parse height input, supporting either meters (e.g. 1.75) or centimeters (e.g. 175)."""
    val = float(raw_input.strip())
    if val <= 0:
        raise ValueError("Height must be positive.")
    # If height > 3.0, assume user provided cm and convert to meters
    if val > 3.0:
        val = val / 100.0
    if val < 0.5 or val > 2.8:
        raise ValueError(f"Height {val:.2f}m is outside plausible human range (0.5m - 2.8m).")
    return val


def parse_weight(raw_input: str) -> float:
    """Parse weight input in kilograms."""
    val = float(raw_input.strip())
    if val <= 0:
        raise ValueError("Weight must be positive.")
    if val < 10.0 or val > 500.0:
        raise ValueError(f"Weight {val:.1f}kg is outside plausible human range (10kg - 500kg).")
    return val


def display_report(height_m: float, weight_kg: float, bmi: float) -> None:
    """Format and print BMI summary report."""
    category, advice = get_bmi_category(bmi)
    ideal_min, ideal_max = get_ideal_weight_range(height_m)
    
    print("\n" + "=" * 50)
    print("               BMI REPORT SUMMARY               ")
    print("=" * 50)
    print(f" Height        : {height_m * 100:.1f} cm ({height_m:.2f} m)")
    print(f" Weight        : {weight_kg:.1f} kg")
    print(f" BMI           : {bmi:.2f}")
    print(f" Category      : {category}")
    print(f" Ideal Weight  : {ideal_min} kg ~ {ideal_max} kg")
    print("-" * 50)
    print(f" Health Advice : {advice}")
    print("=" * 50 + "\n")


def prompt_float(prompt_text: str, parser_func) -> float:
    """Repeatedly prompt user until valid input is received or user enters 'q'."""
    while True:
        user_val = input(prompt_text).strip()
        if user_val.lower() in ("q", "quit", "exit"):
            raise KeyboardInterrupt
        try:
            return parser_func(user_val)
        except ValueError as err:
            print(f" [!] Invalid input: {err}. Please try again (or enter 'q' to quit).")


def main() -> None:
    """Main interactive command-line interface."""
    print("=" * 50)
    print("           Welcome to the BMI Calculator          ")
    print("=" * 50)
    print("Type 'q' or 'exit' anytime to quit.\n")

    while True:
        try:
            height = prompt_float("Enter your height (in cm or meters, e.g. 175 or 1.75): ", parse_height)
            weight = prompt_float("Enter your weight (in kg, e.g. 68.5): ", parse_weight)
            
            bmi = calculate_bmi(weight, height)
            display_report(height, weight, bmi)

            again = input("Would you like to calculate another? (Y/n): ").strip().lower()
            if again in ("n", "no", "q", "quit", "exit"):
                print("Thank you for using BMI Calculator. Stay healthy!")
                break
            print()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting BMI Calculator. Goodbye!")
            break


if __name__ == "__main__":
    main()
