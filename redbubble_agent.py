
import os,json,random
from PIL import Image,ImageDraw
from io import BytesIO
from playwright.sync_api import sync_playwright
COOKIES=os.getenv("REDBUBBLE_COOKIES")
def upload(cookies):
    img=Image.new("RGB",(2000,2000),(random.randint(0,255),)*3)
    d=ImageDraw.Draw(img)
    for _ in range(50): x1,y1,x2,y2=[random.randint(0,2000) for _ in range(4)]; d.line((x1,y1,x2,y2),fill=(random.randint(0,255),)*3,width=5)
    buf=BytesIO(); img.save(buf,format="PNG"); buf.seek(0)
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(cookies));pg=ctx.new_page()
        pg.goto("https://www.redbubble.com/portfolio/images/new"); pg.set_input_files("input[type='file']",buf); time.sleep(5)
        pg.fill("input[name='work_title']",f"Genesis Design {{random.randint(1000,9999)}}"); pg.fill("textarea[name='work_description']","Abstract design")
        pg.fill("input[name='work_tags']","abstract,modern,art"); pg.click("button:has-text('Save')"); time.sleep(3); b.close()
def main():
    if COOKIES: upload(COOKIES)
if __name__=="__main__": main()
