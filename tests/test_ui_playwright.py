from __future__ import annotations

#(ทดสอบกรณี Login สำเร็จ) เราจะใช้ Playwright เพื่อจำลองการเปิดหน้าเว็บ, กรอกข้อมูล username และ password ที่ถูกต้อง, แล้วกดปุ่ม Login จากนั้นเราจะตรวจสอบว่าเราเข้าสู่ระบบสำเร็จโดยดูว่ามีข้อความต้อนรับ (Welcome) ปรากฏขึ้นหรือเปล่า ซึ่งเป็นสัญญาณว่าเราได้เข้าสู่ Dashboard ของผู้ใช้แล้ว
def test_login_success(page, base_url: str):
    page.goto(f"{base_url}/")
    page.fill("#username", "admin")
    page.fill("#password", "secret123")
    page.get_by_role("button", name="Login").click()

    assert page.get_by_text("Dashboard").is_visible()
    assert page.get_by_text("Welcome admin").is_visible()


#(ทดสอบกรณี Login ล้มเหลว) เราจะใช้ Playwright เพื่อจำลองการเปิดหน้าเว็บ, กรอกข้อมูล username และ password ที่ผิด, แล้วกดปุ่ม Login จากนั้นเราจะตรวจสอบว่าเกิดข้อผิดพลาดขึ้นโดยดูว่ามีข้อความแสดงข้อผิดพลาด (Invalid credentials) ปรากฏขึ้นหรือเปล่า ซึ่งเป็นสัญญาณว่าเราไม่สามารถเข้าสู่ระบบได้เพราะข้อมูลที่กรอกไม่ถูกต้อง
def test_login_failure(page, base_url: str):
    page.goto(f"{base_url}/")
    page.fill("#username", "admin")
    page.fill("#password", "wrongpass")
    page.get_by_role("button", name="Login").click()

    assert page.locator("#error").is_visible()
    assert page.locator("#error").text_content() == "Invalid credentials"
