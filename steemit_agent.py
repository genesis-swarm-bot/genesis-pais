import os, json, time, requests
from beem import Steem

STEEM_USER = os.getenv("STEEMIT_USERNAME")
STEEM_KEY = os.getenv("STEEMIT_ACTIVE_KEY")
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
    # Pass the active key so beem can sign the transaction
    steem = Steem(keys=[STEEM_KEY])
    steem.post(title, body, author=STEEM_USER, tags=tags)

def main():
    try:
        with open("/tmp/trends.json") as f:
            trends = json.load(f)
    except:
        trends = ["crypto"]
    topic = trends[0] if trends else "crypto"
    article = generate_article(topic)
    if STEEM_USER and STEEM_KEY:
        post(f"How {topic} Works", article, ["crypto", "blog"])

if __name__ == "__main__":
    main()
