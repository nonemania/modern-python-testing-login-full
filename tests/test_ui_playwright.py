from __future__ import annotations


def test_login_success(page, base_url: str):
    page.goto(f"{base_url}/")
    page.fill("#username", "admin")
    page.fill("#password", "secret123")
    page.get_by_role("button", name="Login").click()

    assert page.get_by_text("Dashboard").is_visible()
    assert page.get_by_text("Welcome admin").is_visible()



def test_login_failure(page, base_url: str):
    page.goto(f"{base_url}/")
    page.fill("#username", "admin")
    page.fill("#password", "wrongpass")
    page.get_by_role("button", name="Login").click()

    assert page.locator("#error").is_visible()
    assert page.locator("#error").text_content() == "Invalid credentials"
