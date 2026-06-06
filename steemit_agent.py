import os, json, time, random
from beem import Steem

STEEM_USER = os.getenv("STEEMIT_USERNAME", "genesisai")
STEEM_POSTING_KEY = "5K4Z5JfHh758Put8uc5EtBYmiZ1D8MJxPKJjC3ENERVgJUkti5m"

def article(topic):
    return f"{topic} is changing the crypto landscape. Learn how and why it matters in our latest post."

def main():
    if not STEEM_USER or not STEEM_POSTING_KEY:
        return
    trends = ["crypto", "Bitcoin", "Ethereum"]
    topic = random.choice(trends)
    title = f"How {topic} Works"
    body = article(topic)
    steem = Steem(keys=[STEEM_POSTING_KEY])
    steem.post(title, body, author=STEEM_USER, tags=["crypto", "blog"])

if __name__ == "__main__":
    main()
