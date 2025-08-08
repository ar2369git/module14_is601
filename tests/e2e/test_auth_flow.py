import pytest
from playwright.sync_api import Page
from datetime import datetime


BASE = "http://localhost:8000"

@ pytest.fixture(scope="module")
def credentials():
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "email": f"e2e{ts}@example.com",
        "username": f"e2euser{ts}",
        "password": "password123"
    }

@pytest.mark.e2e
def test_register_flow(page: Page, credentials):
    page.goto(f"{BASE}/register.html")
    page.fill("input[name='email']", credentials["email"])
    page.fill("input[name='username']", credentials["username"])
    page.fill("input[name='password']", credentials["password"])
    page.fill("input[name='confirm_password']", credentials["password"])
    # submit the registration form
    page.click("form#register-form button[type=submit]")
    # should display a success message
    page.wait_for_selector("#message:has-text('Registration successful')", timeout=5000)

@pytest.mark.e2e
def test_login_flow(page: Page, credentials):
    page.goto(f"{BASE}/login.html")
    page.fill("input[name='username_or_email']", credentials["username"])
    page.fill("input[name='password']", credentials["password"])
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("form#login-form button[type=submit]")
    # auth.js redirects to home on success
    page.wait_for_url(f"{BASE}/", timeout=5000)

@pytest.mark.e2e
def test_login_invalid(page: Page, credentials):
    page.goto(f"{BASE}/login.html")
    page.fill("input[name='username_or_email']", credentials["username"])
    page.fill("input[name='password']", "wrongpass")
    page.click("form#login-form button[type=submit]")
    # invalid login shows error in the message div
    page.wait_for_selector("#message:has-text('Invalid credentials')", timeout=5000)
