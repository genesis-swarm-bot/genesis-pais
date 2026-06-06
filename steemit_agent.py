import os, json, time, requests, sys
from beem import Steem

STEEM_USER = os.getenv("STEEMIT_USERNAME")
STEEM_POSTING_KEY = os.getenv("STEEMIT_POSTING_KEY")
NC_WALLET = os.getenv("NC_WALLET_ETH", "0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419")

def generate_article(topic):
    try:
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN', '')}"}
        prompt = f"Write a Steemit post about {topic}"
        resp = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
        if resp.status_code == 200:
            return resp.json()[0]["generated_text"]
    except Exception as e:
        print(f"Hugging Face API error (using fallback): {e}")
    return f"{topic} is changing the crypto landscape. Learn how and why it matters in our latest post."

def post(title, body, tags):
    if not STEEM_POSTING_KEY:
        print("ERROR: STEEMIT_POSTING_KEY is missing or empty.")
        sys.exit(1)
    steem = Steem(keys=[STEEM_POSTING_KEY])
    steem.post(title, body, author=STEEM_USER, tags=tags)

def main():
    if not STEEM_USER or not STEEM_POSTING_KEY:
        print("Missing STEEMIT_USERNAME or STEEMIT_POSTING_KEY – skipping post.")
        return

    try:
        with open("/tmp/trends.json") as f:
            trends = json.load(f)
    except:
        trends = ["crypto"]
    topic = trends[0] if trends else "crypto"
    article = generate_article(topic)
    post(f"How {topic} Works", article, ["crypto", "blog"])

if __name__ == "__main__":
    main()
