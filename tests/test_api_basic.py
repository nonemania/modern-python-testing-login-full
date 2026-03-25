from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

# TestClient เปรียบเสมือน "หุ่นยนต์จำลอง Browser" ที่สร้างขึ้นมาเพื่อคุยกับ FastAPI
# ใช้ TestClient ของ FastAPI และรันผ่าน Pytest เพื่อให้มั่นใจว่า API ทำงานถูกต้องทุกครั้งที่รันคำสั่ง โดยไม่ต้องมานั่งจิ้มทดสอบเองทีละอัน
client = TestClient(app)

#เช็คว่า "เซิร์ฟเวอร์ยังฟื้นอยู่ไหม" เหมือนการเคาะประตูบ้านแล้วมีคนตอบว่า "อยู่ครับ" (Status 200 OK) และยังเช็คด้วยว่า Response Body ตอบกลับมาถูกต้องตามที่เราคาดหวังหรือเปล่า
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

#เช็คกรณี "เข้าสู่ระบบสำเร็จ" โดยส่ง ID/Password ที่ถูกต้องเข้าไป แล้วต้องได้กุญแจ (Token) กลับมาเพื่อใช้ในการเข้าถึงข้อมูลส่วนตัวของผู้ใช้ในอนาคต
def test_api_login_success():
    response = client.post(
        "/api/login",
        json={"username": "admin", "password": "secret123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "login success"
    assert "token" in data

#เช็คกรณี "ใส่รหัสผิด" ระบบต้องใจแข็งไม่ให้เข้า (401 Unauthorized) และบอกว่าข้อมูลผิดนะ (invalid credentials) เพื่อให้ผู้ใช้รู้ว่าต้องเช็ค ID/Password อีกที
def test_api_login_invalid_credentials():
    response = client.post(
        "/api/login",
        json={"username": "admin", "password": "wrongpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"

#เช็คกรณี "ส่งข้อมูลไม่ครบ" เช่น ลืมพิมพ์ชื่อผู้ใช้ FastAPI จะดักตบข้อมูลที่ผิดรูปแบบทิ้งทันที (422 Unprocessable Entity) เพราะมันรู้ว่า "เออ ข้อมูลไม่ครบ" และไม่ต้องไปเสียเวลาตรวจสอบใน Logic ว่าข้อมูลผิดหรือเปล่า
def test_api_login_schema_validation_error():
    response = client.post(
        "/api/login",
        json={"username": "", "password": ""},
    )
    assert response.status_code == 422

#เช็คกรณี "ข้อมูลครบแต่เนื้อหาใช้ไม่ได้" เช่น ใส่ช่องว่าง (Space) มาแทนชื่อ ซึ่งโปรแกรมเมอร์เขียนดักไว้เองว่าแบบนี้ไม่เอา (400 Bad Request) เพราะมันรู้ว่า "เออ ข้อมูลครบ แต่เนื้อหามันไม่ใช่" และไม่ต้องไปเสียเวลาตรวจสอบใน Logic ว่าข้อมูลผิดหรือเปล่า
def test_api_login_invalid_input_but_schema_valid():
    response = client.post(
        "/api/login",
        json={"username": "   ", "password": "1234"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "invalid input"