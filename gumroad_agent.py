import os, json, time
from playwright.sync_api import sync_playwright

COOKIES = os.getenv("GUMROAD_COOKIES")

def sanitize_cookies(raw_cookies):
    valid_same_site = {"Strict", "Lax", "None"}
    cleaned = []
    for c in raw_cookies:
        new_c = {
            "name": c.get("name", ""),
            "value": c.get("value", ""),
            "domain": c.get("domain", ""),
            "path": c.get("path", "/"),
            "secure": c.get("secure", False),
            "httpOnly": c.get("httpOnly", False),
        }
        same_site = c.get("sameSite", "Lax")
        if same_site not in valid_same_site:
            same_site = "Lax"
        new_c["sameSite"] = same_site
        if not c.get("session", False) and "expirationDate" in c:
            new_c["expires"] = float(c["expirationDate"])
        cleaned.append(new_c)
    return cleaned

def create_product(cookies):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(sanitize_cookies(json.loads(cookies)))
        pg = ctx.new_page()
        pg.goto("https://app.gumroad.com/products/new")
        pg.fill("input[name='name']", "AI Insights eBook")
        pg.fill("textarea[name='description']", "A collection of AI-generated insights.")
        pg.fill("input[name='price']", "5")
        pg.click("button:has-text('Create')")
        time.sleep(3)
        b.close()

def main():
    if COOKIES:
        create_product(COOKIES)

if __name__ == "__main__":
    main()
