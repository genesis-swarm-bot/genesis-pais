
import os,json,time
from playwright.sync_api import sync_playwright
COOKIES=os.getenv("GUMROAD_COOKIES")
def create_product(cookies):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(cookies));pg=ctx.new_page()
        pg.goto("https://app.gumroad.com/products/new"); pg.fill("input[name='name']","AI Insights eBook")
        pg.fill("textarea[name='description']","A collection of AI-generated insights."); pg.fill("input[name='price']","5")
        pg.click("button:has-text('Create')"); time.sleep(3); b.close()
def main():
    if COOKIES: create_product(COOKIES)
if __name__=="__main__": main()
