import pytest
from playwright.sync_api import Page

BASE = "http://127.0.0.1:8000"

@pytest.mark.e2e
def test_homepage_and_operations(page: Page):
    page.goto(BASE)
    assert page.inner_text("h1") == "Hello World"

    # do an addition; note that the input names/ids now match the HTML
    page.fill("#a", "2")
    page.fill("#b", "3")

    # operation select now uses the enum value
    page.select_option("#operation", "Add")
    page.click("button#calculate")

    # wait for the result element to populate
    page.wait_for_selector("#result", timeout=5000)
    assert page.inner_text("#result") == "5"
