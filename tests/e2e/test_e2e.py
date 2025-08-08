# tests/e2e/test_e2e.py

import pytest
from playwright.sync_api import Page

BASE = "http://127.0.0.1:8000"

@pytest.mark.e2e
@pytest.mark.skip(reason="Legacy index calculator deprecated; e2e to be rewritten against new UI")
def test_homepage_and_operations(page: Page):
    # first log in with our e2euser
    page.goto(f"{BASE}/login.html")
    page.fill("input[name='username_or_email']", "e2euser")
    page.fill("input[name='password']", "password123")
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("form#auth-form button[type=submit]")
    page.wait_for_url(BASE + "/")
    assert page.inner_text("h1") == "Hello World"

    # now do an addition via the old inline calculator
    page.fill("input[name='a']", "2")
    page.fill("input[name='b']", "3")
    page.select_option("select#operation", "add")
    page.click("button#calculate")
    page.wait_for_selector("text=5")
    assert page.inner_text("#result") == "5"
