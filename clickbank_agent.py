
import os,json,requests,time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
NICKNAME=os.getenv("CLICKBANK_NICKNAME")
WP_URL=os.getenv("WORDPRESS_URL")
WP_COOKIES=os.getenv("WORDPRESS_COOKIES")
TW_COOKIES=os.getenv("TWITTER_COOKIES")
def fetch_products():
    r=requests.get("https://www.clickbank.com/feeds/marketplace_feed_v1.xml")
    soup=BeautifulSoup(r.content,"xml")
    return [(it.find("title").text, it.find("link").text) for it in soup.find_all("item")[:3]]
def post_blog(title,content):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(WP_COOKIES));pg=ctx.new_page()
        pg.goto(f"{WP_URL}/wp-admin/post-new.php")
        pg.fill("textarea#title",title); pg.fill("textarea#content",content); pg.click("input#publish"); time.sleep(2); b.close()
def tweet(content):
    if not TW_COOKIES: return
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True);ctx=b.new_context();ctx.add_cookies(json.loads(TW_COOKIES));pg=ctx.new_page()
        pg.goto("https://twitter.com/compose/tweet"); pg.fill("div[data-testid='tweetTextarea_0']",content[:280])
        pg.click("div[data-testid='tweetButton']"); time.sleep(2); b.close()
def main():
    if not NICKNAME: return
    for name,link in fetch_products():
        aff_link=link+"?hop="+NICKNAME
        review=requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            headers={"Authorization":f"Bearer {os.getenv('HF_TOKEN','')}"}, json={"inputs":f"Write a short review for {name} and include the link {aff_link}"}).json()[0]["generated_text"]
        if WP_COOKIES: post_blog(name,review)
        if TW_COOKIES: tweet(f"Check out {name}: {aff_link}")
if __name__=="__main__": main()
