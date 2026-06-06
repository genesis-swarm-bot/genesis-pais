import os, json, time, requests
from playwright.sync_api import sync_playwright

NC_WALLET = os.getenv("NC_WALLET_ETH", "0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419")

def generate_article(topic):
    try:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN', '')}"}
        prompt = f"Write a short crypto blog post about {topic}"
        resp = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
        if resp.status_code == 200:
            return resp.json()[0]["generated_text"]
    except Exception as e:
        print(f"Hugging Face API error (using fallback): {e}")
    return f"{topic} continues to make waves in the crypto world. Stay tuned for more insights and updates."

def post(title, body, cookies):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(json.loads(cookies))
        pg = ctx.new_page()
        pg.goto("https://www.publish0x.com/new")
        pg.fill("input[name='title']", title)
        pg.fill("div.ql-editor", body)
        pg.click("button:has-text('Publish')")
        time.sleep(3)
        b.close()

def withdraw(cookies):
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        ctx.add_cookies(json.loads(cookies))
        pg = ctx.new_page()
        pg.goto("https://www.publish0x.com/account/wallet")
        bal = pg.text_content(".wallet-balance")
        if bal and float(bal.replace("$", "").strip()) > 5:
            pg.click("text=Withdraw")
            pg.fill("input[name='wallet_address']", NC_WALLET)
            pg.click("button:has-text('Confirm')")
            time.sleep(2)
        b.close()

def main():
    try:
        with open("/tmp/trends.json") as f:
            trends = json.load(f)
    except:
        trends = ["crypto"]
    topic = trends[0] if trends else "crypto"
    title = f"How {topic} Is Changing Crypto"
    article = generate_article(topic)
    cookies = os.getenv("PUBLISH0X_COOKIES")
    if cookies:
        post(title, article, cookies)
        withdraw(cookies)

if __name__ == "__main__":
    main()
