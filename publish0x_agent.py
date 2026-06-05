
import os,json,time,requests
from playwright.sync_api import sync_playwright
NC_WALLET="0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419"
def post(title,body,cookies):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); ctx=b.new_context(); ctx.add_cookies(json.loads(cookies)); pg=ctx.new_page()
        pg.goto("https://www.publish0x.com/new"); pg.fill("input[name='title']",title); pg.fill("div.ql-editor",body)
        pg.click("button:has-text('Publish')"); time.sleep(3); b.close()
def withdraw(cookies):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(cookies));pg=ctx.new_page()
        pg.goto("https://www.publish0x.com/account/wallet")
        bal=pg.text_content(".wallet-balance")
        if bal and float(bal.replace("$","").strip())>5:
            pg.click("text=Withdraw"); pg.fill("input[name='wallet_address']",NC_WALLET); pg.click("button:has-text('Confirm')"); time.sleep(2)
        b.close()
def main():
    try:
        with open("/tmp/trends.json") as f: trends=json.load(f)
    except: trends=["crypto"]
    t=trends[0]
    article=requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1", headers={"Authorization":f"Bearer {os.getenv('HF_TOKEN','')}"}, json={"inputs":f"Write a short crypto blog post about {t}"}).json()[0]["generated_text"]
    cookies=os.getenv("PUBLISH0X_COOKIES")
    if cookies: post(f"How {t} Is Changing Crypto",article,cookies); withdraw(cookies)
if __name__=="__main__": main()
