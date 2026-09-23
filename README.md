# BMI Calculator (v2.1 - Multilingual)

An interactive, user-friendly Command-Line Interface (CLI) Body Mass Index (BMI) calculator built in Python with multilingual support:
- **English** (`en`)
- **Traditional Chinese / 繁體中文** (`zh-tw`)
- **Japanese / 日本語** (`ja`)
- **Korean / 한국어** (`ko`)

## Features
- **Multilingual Interface**: Seamlessly switch between 4 languages.
- **Flexible Language Selection**:
  - Interactive selection prompt on launch.
  - Command-line argument support (`--lang en`, `--lang zh-tw`, `--lang ja`, `--lang ko`).
- **Flexible Height Input**: Accepts input in centimeters (e.g., `175`) or meters (e.g., `1.75`).
- **Comprehensive Analysis**:
  - Calculates BMI value (\(BMI = \frac{weight}{height^2}\)).
  - Identifies health category according to WHO & Asian regional standards.
  - Suggests healthy ideal weight range for your height.
  - Provides actionable lifestyle and health tips.
- **Robust Input Validation**: Localized error messages for invalid or out-of-range inputs.
- **Loop / Quit Anytime**: Type `q` or `exit` anytime to leave.

## Getting Started

### Prerequisites
- Python 3.8+ (tested with Python 3.13)

### How to Run

#### Interactive Mode (prompts to choose language):
```bash
python bmi_calculator.py
```

#### Launch Directly in a Specific Language:
```bash
# Traditional Chinese (繁體中文)
python bmi_calculator.py --lang zh-tw

# Japanese (日本語)
python bmi_calculator.py --lang ja

# Korean (한국어)
python bmi_calculator.py --lang ko

# English
python bmi_calculator.py --lang en
```

### Running Unit Tests
```bash
python -m unittest test_bmi_calculator.py
```

## BMI Categories Reference

| BMI Range | English | 繁體中文 | 日本語 | 한국어 |
| :--- | :--- | :--- | :--- | :--- |
| `< 18.5` | Underweight | 體重過輕 | 低体重・やせ型 | 저체중 |
| `18.5 ~ 23.9` | Normal Weight | 正常體位 | 普通体重 | 정상 체중 |
| `24.0 ~ 26.9` | Overweight | 過重 | 肥満予備軍・過体重 | 과체중 |
| `27.0 ~ 29.9` | Mild Obesity (Class I) | 輕度肥胖 | 肥満（1度） | 경도 비만 (1단계) |
| `30.0 ~ 34.9` | Moderate Obesity (Class II) | 中度肥胖 | 肥満（2度） | 중등도 비만 (2단계) |
| `≥ 35.0` | Severe Obesity (Class III) | 重度肥胖 | 肥満（3度以上・高度肥満） | 고도 비만 (3단계) |
