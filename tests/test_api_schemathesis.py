from __future__ import annotations

import pytest
import schemathesis
from fastapi.testclient import TestClient

from app.main import app

# Schemathesis คือเครื่องมือทดสอบ API แบบอัตโนมัติขั้นสูง (Modern API Testing Tool) ที่ฉลาดกว่าการเขียน Unit Test ทั่วไป เพราะมันจะอ่าน OpenAPI Schema ของ API ของเรา แล้วสร้างชุดคำขอ (Request) ที่หลากหลายและครอบคลุมทุกกรณีที่เป็นไปได้ เช่น การส่งข้อมูลที่ถูกต้อง, การส่งข้อมูลผิดรูปแบบ, การส่งข้อมูลที่ขาดหายไป, หรือแม้แต่การส่งข้อมูลที่มีความยาวเกินกำหนด เพื่อทดสอบว่า API ของเราจะตอบสนองอย่างไรในแต่ละกรณี และยังตรวจสอบว่า Response ที่ได้กลับมานั้นตรงกับที่ Schema กำหนดไว้หรือเปล่า ซึ่งช่วยให้เรามั่นใจได้ว่า API ของเราทำงานถูกต้องและมีความแข็งแกร่งต่อการใช้งานจริงมากขึ้น
@pytest.fixture(scope="session")
def api_schema():
    """Create schemathesis schema from the FastAPI app."""
    return schemathesis.openapi.from_asgi("/openapi.json", app)

schema = schemathesis.pytest.from_fixture("api_schema")


#ใช้ Schemathesis เพื่อตรวจสอบว่า "โค้ดจริง" กับ "เอกสาร API (Swagger)" ตรงกัน 100% หรือเปล่า เช่น ถ้าเราเปลี่ยนชื่อพารามิเตอร์ในโค้ด แต่ลืมอัปเดตใน OpenAPI Schema ที่เราเขียนไว้ใน Swagger แล้วล่ะก็ Schemathesis จะจับผิดได้ทันทีว่า "เฮ้ย ชื่อพารามิเตอร์ไม่ตรงกับที่เอกสารบอกนะ" และจะทำให้การทดสอบล้มเหลว เพื่อให้เรารู้ว่าต้องไปแก้ไขให้ตรงกันทั้งโค้ดและเอกสาร ซึ่งช่วยป้องกันปัญหาที่เกิดจากการที่โค้ดและเอกสารไม่สอดคล้องกัน (API Contract Violation) ที่อาจทำให้ผู้ใช้ API สับสนหรือใช้งานผิดพลาดได้
@schema.parametrize()
def test_api_contract(case):
    """Test API contract compliance using property-based testing with schemathesis.
    
    This test verifies that:
    - All endpoints respond according to their OpenAPI schema
    - Request/response formats match the documented API contract
    - Proper status codes are returned
    """
    with TestClient(app) as client:
        try:
            case.call_and_validate(session=client)
        except Exception as e:
            # Provide more detailed error information for debugging
            pytest.fail(f"Schemathesis test failed for {case.method} {case.formatted_path}: {e}")


# Additional test to verify specific login scenarios
#ใช้ตารางข้อมูล (Table-driven test) วนลูปส่งค่าเข้าไปในฟังก์ชันเดียว เพื่อทดสอบกรณีต่างๆ ที่เราคาดหวังไว้ เช่น กรณีที่ข้อมูลถูกต้อง, กรณีที่ข้อมูลผิด, กรณีที่ข้อมูลขาดหายไป, หรือกรณีที่ข้อมูลมีความยาวเกินกำหนด ซึ่งช่วยให้เราทดสอบได้ครอบคลุมและชัดเจนมากขึ้น โดยไม่ต้องเขียนฟังก์ชันทดสอบแยกกันหลายๆ อัน และยังช่วยให้เราเห็นภาพรวมของกรณีทดสอบทั้งหมดได้ง่ายขึ้นในครั้งเดียว
@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "secret123", 200),           # Valid credentials
    ("invalid", "invalid", 401),           # Invalid credentials  
    ("", "secret123", 422),                # Empty username (validation error)
    ("admin", "", 422),                    # Empty password (validation error)
    ("admin", "x", 422),                   # Too short password (validation error)
    ("a" * 51, "secret123", 422),          # Too long username (validation error)
])
def test_login_validation(username, password, expected_status):
    """Test specific login validation scenarios explicitly."""
    with TestClient(app) as client:
        response = client.post("/api/login", json={"username": username, "password": password})
        assert response.status_code == expected_status
