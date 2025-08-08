# tests/e2e/test_e2e.py

import pytest
from playwright.sync_api import Page

BASE = "http://127.0.0.1:8000"

@pytest.mark.e2e
@pytest.mark.skip(reason="Legacy index calculator deprecated; e2e to be rewritten against new UI")
def test_homepage_and_operations(page: Page):
    page.goto(BASE)
    assert page.inner_text("h1") == "Hello World"

    # do an addition
    page.fill("input[name='a']", "2")
    page.fill("input[name='b']", "3")
    page.select_option("select#operation", "add")
    page.click("button#calculate")
    page.wait_for_selector("#result:has-text('5')", timeout=5000)
    assert page.inner_text("#result") == "5"
