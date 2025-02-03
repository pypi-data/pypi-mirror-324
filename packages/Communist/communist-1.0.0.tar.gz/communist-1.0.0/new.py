from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    with open(r"D:\browser-use\Fireflink_NLP\browser\test.js") as f:
        js_script = f.read()
    page.add_init_script(js_script)
    page.goto('https://www.amazon.com')
    # page.wait_for_timeout(500000)
    page.wait_for_timeout(20000)
    page.wait_for_selector('#captchacharacters')
    page.
    page.click('#captchacharacters')
    print(page.evaluate("window.XpathObject"))
    print(page.evaluate("window.ff"))
    # page.wait_for_timeout(500000)
    page.wait_for_timeout(20000)
    page.fill('#captchacharacters', 'Playwright')
    print(page.evaluate("window.XpathObject"))
    # Wait for some time to see the result
    page.wait_for_timeout(2000)

    # Close the browser
    browser.close()
