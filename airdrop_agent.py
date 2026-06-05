
import os,time,requests
from playwright.sync_api import sync_playwright
NC_WALLET="0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419"
def claim(url):
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True); pg=b.new_page()
        pg.goto(url); time.sleep(5); b.close()
def main():
    try:
        r=requests.get("https://api.airdropalert.com/v1/airdrops?filter=free")
        for a in r.json()[:3]: claim(a['url'])
    except: pass
if __name__=="__main__": main()
