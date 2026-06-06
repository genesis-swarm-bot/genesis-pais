import os, json, time
from playwright.sync_api import sync_playwright

COOKIES = os.getenv("GUMROAD_COOKIES")

def sanitize_cookies(raw):
    valid = {"Strict","Lax","None"}
    cleaned = []
    for c in raw:
        new = {"name":c.get("name",""),"value":c.get("value",""),"domain":c.get("domain",""),
               "path":c.get("path","/"),"secure":c.get("secure",False),"httpOnly":c.get("httpOnly",False)}
        s = c.get("sameSite","Lax")
        new["sameSite"] = s if s in valid else "Lax"
        if not c.get("session") and "expirationDate" in c:
            new["expires"] = float(c["expirationDate"])
        cleaned.append(new)
    return cleaned

def main():
    if not COOKIES:
        return
    cookies = sanitize_cookies(json.loads(COOKIES))
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(cookies)
        pg = ctx.new_page()
        pg.goto("https://app.gumroad.com/products/new", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector("input[name='name']", timeout=30000)
        pg.fill("input[name='name']", "AI Insights eBook")
        pg.fill("textarea[name='description']", "A collection of AI-generated insights.")
        pg.fill("input[name='price']", "5")
        pg.click("button:has-text('Create')")
        time.sleep(3)
        b.close()

if __name__ == "__main__":
    main()
