import os, json, time, random, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

COOKIES = os.getenv("REDBUBBLE_COOKIES")

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
    img = Image.new("RGB",(2000,2000),(random.randint(0,255),)*3)
    d = ImageDraw.Draw(img)
    for _ in range(50):
        x1,y1,x2,y2 = [random.randint(0,2000) for _ in range(4)]
        if x1>x2: x1,x2=x2,x1
        if y1>y2: y1,y2=y2,y1
        d.line((x1,y1,x2,y2),fill=(random.randint(0,255),)*3,width=5)
    tmp = os.path.join(tempfile.gettempdir(),"rb_design.png")
    img.save(tmp)

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(cookies)
        pg = ctx.new_page()
        pg.goto("https://www.redbubble.com/portfolio/images/new", wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_selector("input[type='file']", timeout=30000)
        pg.set_input_files("input[type='file']", tmp)
        time.sleep(5)
        pg.fill("input[name='work_title']",f"Genesis Design {random.randint(1000,9999)}")
        pg.fill("textarea[name='work_description']","Abstract digital design")
        pg.fill("input[name='work_tags']","abstract, modern, art")
        pg.click("button:has-text('Save')")
        time.sleep(3)
        b.close()
    os.remove(tmp)

if __name__ == "__main__":
    main()
