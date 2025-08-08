import pytest
from playwright.sync_api import Page

BASE = "http://localhost:8000"

@pytest.mark.e2e
def test_login_flow(page: Page):
    page.goto(f"{BASE}/login.html")

    # Fill in credentials
    page.fill("input[name='username_or_email']", "e2euser")
    page.fill("input[name='password']", "password123")
    page.click("form#login-form button[type=submit]")

    # Wait for redirect back to homepage
    page.wait_for_url(BASE + "/")
    assert page.url.rstrip("/") == BASE

    # Confirm token was saved to localStorage
    token = page.evaluate("() => localStorage.getItem('token')")
    assert token is not None and token != ""

@pytest.mark.e2e
def test_login_invalid(page: Page):
    page.goto(f"{BASE}/login.html")

    # Wrong password
    page.fill("input[name='username_or_email']", "e2euser")
    page.fill("input[name='password']", "wrongpass")
    page.click("form#login-form button[type=submit]")

    # Should stay on login page and show an error message
    page.wait_for_selector("text=Invalid credentials", timeout=5000)
    assert "Invalid credentials" in page.inner_text("body")
