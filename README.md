# BMI Calculator (CLI)

An interactive, user-friendly Command-Line Interface (CLI) Body Mass Index (BMI) calculator built in Python.

## Features
- **Flexible Height Input**: Accepts input in centimeters (e.g., `175`) or meters (e.g., `1.75`).
- **Comprehensive Analysis**:
  - Calculates BMI value (\(BMI = \frac{weight}{height^2}\)).
  - Identifies health category according to WHO & MOHW standards.
  - Suggests healthy ideal weight range for your height.
  - Provides actionable lifestyle and health tips.
- **Robust Input Validation**: Safely handles non-numeric and out-of-range values.
- **Loop / Quit Anytime**: Type `q` or `exit` anytime to leave.

## Getting Started

### Prerequisites
- Python 3.8+ (tested with Python 3.13)

### How to Run
```bash
python bmi_calculator.py
```

### Running Unit Tests
```bash
python -m unittest test_bmi_calculator.py
```

## BMI Categories (WHO / MOHW Guidelines)

| BMI Range | Category |
| :--- | :--- |
| `< 18.5` | Underweight (體重過輕) |
| `18.5 ~ 23.9` | Normal Weight (健康體位) |
| `24.0 ~ 26.9` | Overweight (過重) |
| `27.0 ~ 29.9` | Mild Obesity (輕度肥胖) |
| `30.0 ~ 34.9` | Moderate Obesity (中度肥胖) |
| `≥ 35.0` | Severe Obesity (重度肥胖) |
