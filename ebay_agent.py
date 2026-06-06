import os, json, time
from playwright.sync_api import sync_playwright

COOKIES = os.getenv("EBAY_COOKIES")

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

def main():
    if COOKIES:
        # eBay agent placeholder – currently just logs in and prints a message
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            ctx = b.new_context()
            ctx.add_cookies(sanitize_cookies(json.loads(COOKIES)))
            pg = ctx.new_page()
            pg.goto("https://partnernetwork.ebay.com")
            print("eBay session loaded")
            time.sleep(3)
            b.close()

if __name__ == "__main__":
    main()
