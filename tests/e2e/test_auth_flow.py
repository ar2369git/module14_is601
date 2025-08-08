# tests/e2e/test_auth_flow.py

import pytest
from playwright.sync_api import Page

BASE = "http://localhost:8000"

@pytest.mark.e2e
def test_register_flow(page: Page):
    page.goto(f"{BASE}/register.html")
    page.fill("input[name='email']", "e2e@example.com")
    page.fill("input[name='username']", "e2euser")
    page.fill("input[name='password']", "password123")
    page.fill("input[name='confirm_password']", "password123")

    # intercept the JS alert and accept it
    page.once("dialog", lambda dialog: dialog.accept())
    # submit via the single submit button on the auth-form
    page.click("button[type='submit']")

    # after the alert, the script does: window.location.href = "/"
    page.wait_for_url(BASE + "/")

@pytest.mark.e2e
def test_login_flow(page: Page):
    page.goto(f"{BASE}/login.html")
    page.fill("input[name='username_or_email']", "e2euser")
    page.fill("input[name='password']", "password123")

    page.once("dialog", lambda dialog: dialog.accept())
    page.click("button[type='submit']")
    page.wait_for_url(BASE + "/")

@pytest.mark.e2e
def test_login_invalid(page: Page):
    page.goto(f"{BASE}/login.html")
    page.fill("input[name='username_or_email']", "e2euser")
    page.fill("input[name='password']", "wrongpass")

    page.click("button[type='submit']")
    # the error message is now rendered into the <div id="error">
    page.wait_for_selector("#error:has-text('Invalid credentials')", timeout=5000)
