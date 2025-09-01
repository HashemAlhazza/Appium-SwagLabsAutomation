# 🧪 Swag Labs App Testing (Appium + Python + Pytest)

This project demonstrates automated mobile application testing of the **Swag Labs** sample app using **Appium**, the **Python client library**, and **Pytest**. The tests are executed on an **Android Virtual Device (Pixel 3a API 35)** in **Android Studio** and leverage the **UiAutomator2** automation framework.

---

## 📌 Project Structure

```
.
├── Tests/
│   ├── test_one.py        # Positive test cases
│   └── test_negative.py   # Negative/expected failing cases
│
├── allure-report/         # Generated Allure test reports
├── SwagLabs.apk           # Application under test (edit path in capabilities)
├── requirements.txt
└── README.md
```

---

## ✨ Features

- ✅ Positive and negative test scenarios
- 📱 Android gestures: **Swipe**, **Scroll**, and **Start Activity**
- ⚙️ Each test runs in an isolated app session to ensure independence
- 📊 **Allure** test reports are generated for clear results
- 🧩 Uses the **UiAutomator2** platform for Android automation

---

## ⚡ Tech Stack

- **Language**: Python
- **Frameworks**: Appium, Pytest
- **Automation Engine**: UiAutomator2
- **Device**: Android Virtual Device (Pixel 3a API 35)
- **Reporting**: Allure

---

## 🚀 Setup & Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/swaglabs-appium-tests.git
    cd swaglabs-appium-tests
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure you have an **Appium** server and **Android Studio** installed and configured.)

3. **Configure capabilities**:
    Update the path to the `.apk` file inside the capabilities object in your test files:
    ```json
    "app": "/absolute/path/to/SwagLabs.apk"
    ```

---

## ▶️ Running Tests

To run the positive test cases:
```bash
pytest -s -v Tests/test_one.py
```

To run the negative test cases:
```bash
pytest -s -v Tests/test_negative.py
```

---

## 📊 Generating Reports

This project uses **Allure** for reporting. After running your tests, generate the report by running this command:

```bash
allure serve allure-report/
```

---

## 📜 License

This project is for personal learning and is open for reference.