
import os,json,time,requests
from playwright.sync_api import sync_playwright
BCH_ADDR="qrhzhln53tyz4xn76suj4n52yqnw785ys5kvsav7va"
def post(title,body,cookies):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(cookies));pg=ctx.new_page()
        pg.goto("https://read.cash/create"); pg.fill("input[name='title']",title); pg.fill("div.ql-editor",body)
        pg.click("button[type='submit']"); time.sleep(3); b.close()
def withdraw(cookies):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(cookies));pg=ctx.new_page()
        pg.goto("https://read.cash/wallet")
        bal=float(pg.text_content(".balance-amount").replace("$",""))
        if bal>0.01: pg.click("text=Withdraw"); pg.fill("input[name='address']",BCH_ADDR); pg.fill("input[name='amount']",str(bal)); pg.click("button:has-text('Send')"); time.sleep(3)
        b.close()
def main():
    try:
        with open("/tmp/trends.json") as f: trends=json.load(f)
    except: trends=["crypto"]
    t=trends[0]
    article=requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1", headers={"Authorization":f"Bearer {os.getenv('HF_TOKEN','')}"}, json={"inputs":f"Write an article about {t}"}).json()[0]["generated_text"]
    cookies=os.getenv("READCASH_COOKIES")
    if cookies:
        post(f"How {t} Works",article,cookies)
        withdraw(cookies)
if __name__=="__main__": main()
