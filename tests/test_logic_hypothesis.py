from __future__ import annotations

import string

from hypothesis import assume, given, strategies as st

from app.auth import validate_login_input

USERNAME_CHARS = string.ascii_letters + string.digits + "._-"
PASSWORD_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()_-"


@given(st.text(), st.text())
def test_validate_login_never_crashes(username: str, password: str):
    result = validate_login_input(username, password)
    assert isinstance(result, bool)


@given(
    st.text(alphabet=USERNAME_CHARS, min_size=1, max_size=50),
    st.text(alphabet=PASSWORD_CHARS, min_size=4, max_size=20),
)
def test_validate_login_accepts_reasonable_strings(username: str, password: str):
    assume(username.strip() != "")
    assume(password.strip() != "")
    assert validate_login_input(username, password) is True


@given(st.text(max_size=0), st.text())
def test_empty_username_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False


@given(st.text(alphabet=USERNAME_CHARS, min_size=51), st.text(alphabet=PASSWORD_CHARS, min_size=4, max_size=20))
def test_too_long_username_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False


@given(st.text(alphabet=USERNAME_CHARS, min_size=1, max_size=50), st.text(alphabet=PASSWORD_CHARS, min_size=0, max_size=3))
def test_too_short_password_is_invalid(username: str, password: str):
    assert validate_login_input(username, password) is False
