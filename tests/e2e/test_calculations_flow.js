// tests/e2e/test_calculations_flow.js
import { test, expect } from "@playwright/test";
const BASE = process.env.BASE_URL || "http://localhost:8000";

test.beforeEach(async ({ page }) => {
  // assume user already registered+logged in via auth.js helper
  await page.goto(BASE + "/calculations.html");
});

test("can create and list a calculation", async ({ page }) => {
  await page.fill("input[name=a]", "2");
  await page.fill("input[name=b]", "3");
  await page.selectOption("select[name=type]", "Add");
  await page.click("form#add-form button");
  await expect(page.locator("#message")).toHaveText(/added/i);
  await expect(page.locator("#calc-list")).toContainText("2 Add 3 = 5");
});

test("rejects divide by zero", async ({ page }) => {
  await page.fill("input[name=a]", "1");
  await page.fill("input[name=b]", "0");
  await page.selectOption("select[name=type]", "Divide");
  await page.click("form#add-form button");
  await expect(page.locator("#message")).toContainText("Division by zero");
});
