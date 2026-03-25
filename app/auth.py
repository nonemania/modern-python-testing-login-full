# auth.py - Authentication logic for the login system. 
# การเช็คว่าข้อมูลที่ผู้ใช้กรอกมานั้น "ถูกรูปแบบ" และ "รหัสผ่านถูกต้อง" หรือไม่ ก่อนจะอนุญาตให้เข้าหน้า Dashboard ได้
from __future__ import annotations


def validate_login_input(username: str | None, password: str | None) -> bool:
    """Basic validation for the login form.

    This is intentionally simple for classroom/demo purposes.
    """
    if username is None or password is None:
        return False

    username = username.strip()
    password = password.strip()

    if not username or not password:
        return False

    if len(username) > 50:
        return False

    if len(password) < 4 or len(password) > 20:
        return False

    return True


USERS = {
    "admin": "secret123",
    "teacher": "python123",
}


def authenticate(username: str, password: str) -> bool:
    expected = USERS.get(username)
    return expected == password
