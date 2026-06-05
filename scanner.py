
import requests, json
def main():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/search/trending")
        coins = [c["item"]["name"] for c in r.json()["coins"]]
        with open("/tmp/trends.json","w") as f: json.dump(coins[:5], f)
    except: pass
if __name__=="__main__": main()
