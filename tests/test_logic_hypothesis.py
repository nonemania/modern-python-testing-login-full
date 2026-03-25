from __future__ import annotations

import string

from hypothesis import assume, given, strategies as st

from app.auth import validate_login_input

#กำหนดชุดตัวอักษรที่ระบบเรา "อนุญาต" (Whitelist) เช่น ตัวอักษรภาษาอังกฤษ, ตัวเลข และสัญลักษณ์บางตัวที่มักใช้ใน username และ password เพื่อให้การทดสอบมีความสมจริงและตรงกับความต้องการของระบบมากขึ้น
USERNAME_CHARS = string.ascii_letters + string.digits + "._-"
PASSWORD_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()_-"


#Robustness Testing (การทดสอบความแข็งแกร่งของระบบ) st.text() แบบไม่ใส่ Parameter จะไม่ได้สุ่มแค่ "abc" หรือ "123" แต่มันจะสุ่ม Unicode ทุกประเภท รวมถึง Emoji, อักษรภาษาอาหรับ, ช่องว่างแปลกๆ, หรือแม้แต่ Null bytes (\x00) ซึ่งมักเป็นสาเหตุที่ทำให้ Database หรือ Logic หลังบ้านพังได้
@given(st.text(), st.text())
def test_validate_login_never_crashes(username: str, password: str):
    result = validate_login_input(username, password)
    assert isinstance(result, bool)

#การทดสอบด้วยข้อมูลที่ถูกต้อง (Positive Testing) เราจะใช้ชุดตัวอักษรที่เรากำหนดไว้ใน USERNAME_CHARS และ PASSWORD_CHARS เพื่อสร้าง username และ password ที่มีความยาวเหมาะสมและไม่มีช่องว่างที่เป็นปัญหา เช่น "user.name_123" หรือ "P@ssw0rd!" ซึ่งเป็นรูปแบบที่ผู้ใช้จริงๆ มักจะใช้ และเราจะตรวจสอบว่า validate_login_input() คืนค่า True สำหรับข้อมูลเหล่านี้
@given(
    st.text(alphabet=USERNAME_CHARS, min_size=1, max_size=50),
    st.text(alphabet=PASSWORD_CHARS, min_size=4, max_size=20),
)
def test_validate_login_accepts_reasonable_strings(username: str, password: str):
    assume(username.strip() != "")
    assume(password.strip() != "")
    assert validate_login_input(username, password) is True

#การทดสอบกรณี Username เป็นค่าว่าง (Negative Testing) เราจะใช้ st.text(max_size=0) เพื่อสร้าง username ที่เป็นสตริงว่างเปล่า และ st.text() สำหรับ password เพื่อให้ได้รหัสผ่านที่หลากหลาย จากนั้นเราจะตรวจสอบว่า validate_login_input() คืนค่า False สำหรับกรณีนี้ เนื่องจากระบบควรปฏิเสธการเข้าสู่ระบบที่ไม่มีชื่อผู้ใช้
@given(st.text(max_size=0), st.text())
def test_empty_username_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False

#การทดสอบกรณี Username ยาวเกินกำหนด (Boundary Testing) เราจะใช้ st.text(alphabet=USERNAME_CHARS, min_size=51) เพื่อสร้าง username ที่มีความยาวเกิน 50 ตัวอักษร ซึ่งเป็นขีดจำกัดที่ระบบกำหนดไว้ จากนั้นเราจะตรวจสอบว่า validate_login_input() คืนค่า False สำหรับกรณีนี้ เนื่องจากระบบควรปฏิเสธการเข้าสู่ระบบที่มีชื่อผู้ใช้ยาวเกินไป
@given(st.text(alphabet=USERNAME_CHARS, min_size=51), st.text(alphabet=PASSWORD_CHARS, min_size=4, max_size=20))
def test_too_long_username_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False

#การทดสอบกรณี Password สั้นเกินไป (Security Policy Testing) เราจะใช้ st.text(alphabet=PASSWORD_CHARS, max_size=3) เพื่อสร้าง password ที่มีความยาวไม่ถึง 4 ตัวอักษร ซึ่งเป็นขีดจำกัดที่ระบบกำหนดไว้ จากนั้นเราจะตรวจสอบว่า validate_login_input() คืนค่า False สำหรับกรณีนี้ เนื่องจากระบบควรปฏิเสธการเข้าสู่ระบบที่มีรหัสผ่านสั้นเกินไป
@given(st.text(alphabet=USERNAME_CHARS, min_size=1, max_size=50), st.text(alphabet=PASSWORD_CHARS, min_size=0, max_size=3))
def test_too_short_password_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False
