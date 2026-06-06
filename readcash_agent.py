import os, json, time, random, requests
from playwright.sync_api import sync_playwright

COOKIES = os.getenv("READCASH_COOKIES")
BCH_ADDR = os.getenv("BCH_ADDRESS","qrhzhln53tyz4xn76suj4n52yqnw785ys5kvsav7va")

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
    return f"How {topic} Works: {topic} is a hot topic right now. Here's why it matters."

def main():
    if not COOKIES:
        return
    cookies = sanitize_cookies(json.loads(COOKIES))
    trends = ["crypto","Bitcoin","Ethereum"]
    topic = random.choice(trends)
    body = article(topic)
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(cookies)
        pg = ctx.new_page()
        pg.goto("https://read.cash/create", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector("input[name='title']", timeout=30000)
        pg.fill("input[name='title']", f"How {topic} Works")
        pg.fill("div.ql-editor", body)
        pg.click("button[type='submit']")
        time.sleep(3)
        # Withdraw BCH
        pg.goto("https://read.cash/wallet")
        try:
            bal = float(pg.text_content(".balance-amount").replace("$",""))
            if bal > 0.01:
                pg.click("text=Withdraw")
                pg.fill("input[name='address']", BCH_ADDR)
                pg.fill("input[name='amount']", str(bal))
                pg.click("button:has-text('Send')")
                time.sleep(3)
        except: pass
        b.close()

if __name__ == "__main__":
    main()
