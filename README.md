# From Logic to Browser: Modern Python Testing in VS Code

A full demo project for presenting **smarter login testing** with:

- **Hypothesis** for logic / unit testing
- **Schemathesis** for API contract testing
- **Playwright** for UI / browser testing
- **FastAPI** as the demo app
- **pytest** as the shared test runner

## Project structure

```text
modern-python-testing-login-full/
├─ app/
│  ├─ auth.py
│  ├─ main.py
│  └─ templates/
│     └─ login.html
├─ tests/
│  ├─ conftest.py
│  ├─ test_logic_hypothesis.py
│  ├─ test_api_basic.py
│  ├─ test_api_schemathesis.py
│  └─ test_ui_playwright.py
├─ .vscode/settings.json
├─ pytest.ini
├─ requirements.txt
├─ .gitignore
└─ scripts/
```

## 1) Open the project in VS Code

Open the project folder directly in VS Code.

## 2) Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 3) Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
```

## 4) Run the FastAPI app

```powershell
uvicorn app.main:app --reload
```

Open these URLs:

- App: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

Demo login account:

- username: `admin`
- password: `secret123`

## 5) Run all tests

```powershell
pytest -v
```

## 6) Run each test group separately

### Hypothesis (logic / unit)

```powershell
pytest -v tests/test_logic_hypothesis.py
```

### Basic API tests

```powershell
pytest -v tests/test_api_basic.py
```

### Schemathesis API contract tests

```powershell
pytest -v tests/test_api_schemathesis.py
```

### Playwright UI tests

```powershell
pytest -v tests/test_ui_playwright.py
```

## 7) VS Code Test Explorer

1. Install the **Python** extension.
2. Open the **Testing** view.
3. Choose **Configure Python Tests**.
4. Select **pytest**.
5. VS Code should discover the files inside `tests/`.

## Presentation flow idea

1. Show the login page in the browser.
2. Show `test_logic_hypothesis.py` and explain that Hypothesis generates many inputs automatically.
3. Show `test_api_basic.py` and explain normal API tests.
4. Show `test_api_schemathesis.py` and explain schema-driven API testing.
5. Show `test_ui_playwright.py` and run the browser test live.

## Notes

- The HTML routes (`/` and `/login`) are hidden from OpenAPI so Schemathesis focuses on the API routes.
- The Playwright tests use a fixture in `tests/conftest.py` that starts the server automatically.
- This project is designed for teaching/demo purposes, not production authentication.

## Compare and Summary Tools
- Hypothesis คือ Python Library สำหรับการทำ Testing ที่เปลี่ยนจากการสุ่มมั่วๆ มาเป็นการสุ่มแบบมีกลยุทธ์ เพื่อหาจุดบกพร่องที่เรานึกไม่ถึง
สรุปคือ มันคือเครื่องมือที่ช่วยให้เราเขียน Test น้อยลง แต่ได้ความมั่นใจในคุณภาพ Software มากขึ้น
- TestClient คือ เครื่องมือที่ช่วยให้เรา "จำลองการใช้งานจริง" (Terminal) โดยไม่ต้องเปิดหน้าเว็บจริงและรวดเร็วกว่าการเทสด้วยมือหลายเท่า
- Schemathesis คิอ เครื่องมือทดสอบ API แบบอัตโนมัติขั้นสูง ที่ฉลาดกว่าการเขียน Unit Test ทั่วไป เหมือนเรา "จ้างบริษัทตรวจบ้าน" เอาเครื่องมือมาสแกนทุกซอกทุกมุมและทำเช็คลิสต์ตรวจสอบความเรียบร้อยแบบเป็นระบบ
- Playwright คือเครื่องมือ Open-source สำหรับการทำ Automated Testing บนเว็บเบราว์เซอร์ (เช่น Chrome, Firefox, Safari) พัฒนาโดย Microsoft จุดเด่นคือทำงานได้รวดเร็วและสามารถโต้ตอบกับหน้าเว็บได้เหมือนที่มนุษย์ทำจริงๆ (คลิก, พิมพ์, รอข้อความปรากฏ)