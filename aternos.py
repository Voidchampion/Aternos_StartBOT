import os
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("ATERNOS_EMAIL")
PASSWORD = os.getenv("ATERNOS_PASSWORD")

def login(page):
    page.goto("https://aternos.org/go/")
    page.fill("input[name='user']", EMAIL)
    page.fill("input[name='password']", PASSWORD)
    page.click("button.login-button")
    page.wait_for_timeout(5000)

def start_server():
    with sync_playwright() as p:
    browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-dev-shm-usage"]
)

        page = browser.new_page()
        login(page)

        page.goto("https://aternos.org/server/")
        page.wait_for_timeout(5000)
        page.click("#start")

        browser.close()
        return "✅ Server starting!"

def stop_server():
    with sync_playwright() as p:
browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-dev-shm-usage"]
)

        page = browser.new_page()
        login(page)

        page.goto("https://aternos.org/server/")
        page.wait_for_timeout(5000)
        page.click("#stop")

        browser.close()
        return "🛑 Server stopped!"
