import os, json, time, random, requests
from playwright.sync_api import sync_playwright

NC_WALLET = os.getenv("NC_WALLET_ETH", "0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419")
COOKIES = os.getenv("PUBLISH0X_COOKIES")

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

def article(topic):
    return f"{topic} continues to reshape the crypto landscape. Here's what you need to know."

def main():
    if not COOKIES:
        return
    cookies = sanitize_cookies(json.loads(COOKIES))
    trends = ["crypto","Bitcoin","Ethereum"]
    topic = random.choice(trends)
    title = f"How {topic} Is Changing the Game"
    body = article(topic)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(cookies)
        pg = ctx.new_page()
        pg.goto("https://www.publish0x.com/new", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector("input[name='title']", timeout=30000)
        pg.fill("input[name='title']", title)
        pg.fill("div.ql-editor", body)
        pg.click("button:has-text('Publish')")
        time.sleep(3)
        # Withdraw
        pg.goto("https://www.publish0x.com/account/wallet")
        try:
            bal = float(pg.text_content(".wallet-balance").replace("$","").strip())
            if bal > 5:
                pg.click("text=Withdraw")
                pg.fill("input[name='wallet_address']", NC_WALLET)
                pg.click("button:has-text('Confirm')")
                time.sleep(2)
        except: pass
        b.close()

if __name__ == "__main__":
    main()
