# BMI Calculator (v2.0 - Bilingual)

An interactive, user-friendly Command-Line Interface (CLI) Body Mass Index (BMI) calculator built in Python with bilingual support for **English** and **Traditional Chinese (繁體中文 / zh-tw)**.

## Features
- **Bilingual Interface**: Seamlessly switch between English and Traditional Chinese (`zh-tw`).
- **Flexible Language Selection**:
  - Interactive selection prompt on launch.
  - Command-line argument support (`--lang en` or `--lang zh-tw`).
- **Flexible Height Input**: Accepts input in centimeters (e.g., `175`) or meters (e.g., `1.75`).
- **Comprehensive Analysis**:
  - Calculates BMI value (\(BMI = \frac{weight}{height^2}\)).
  - Identifies health category according to WHO & Taiwan MOHW standards.
  - Suggests healthy ideal weight range for your height.
  - Provides actionable lifestyle and health tips.
- **Robust Input Validation**: Localized error messages for invalid or out-of-range inputs.
- **Loop / Quit Anytime**: Type `q` or `exit` anytime to leave.

## Getting Started

### Prerequisites
- Python 3.8+ (tested with Python 3.13)

### How to Run

#### Interactive Mode (prompts for language):
```bash
python bmi_calculator.py
```

#### Directly in Traditional Chinese (zh-tw):
```bash
python bmi_calculator.py --lang zh-tw
```

#### Directly in English:
```bash
python bmi_calculator.py --lang en
```

### Running Unit Tests
```bash
python -m unittest test_bmi_calculator.py
```

## BMI Categories (WHO / 衛福部健康標準)

| BMI Range | Category (English) | 體位狀態 (繁體中文) |
| :--- | :--- | :--- |
| `< 18.5` | Underweight | 體重過輕 |
| `18.5 ~ 23.9` | Normal Weight | 正常體位 |
| `24.0 ~ 26.9` | Overweight | 過重 |
| `27.0 ~ 29.9` | Mild Obesity (Class I) | 輕度肥胖 |
| `30.0 ~ 34.9` | Moderate Obesity (Class II) | 中度肥胖 |
| `≥ 35.0` | Severe Obesity (Class III) | 重度肥胖 |
