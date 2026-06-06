import os, json, time, random
from beem import Steem
from beem.account import Account

STEEM_USER = os.getenv("STEEMIT_USERNAME", "genesisai")
STEEM_POSTING_KEY = "5K4Z5JfHh758Put8uc5EtBYmiZ1D8MJxPKJjC3ENERVgJUkti5m"

def article(topic):
    return f"{topic} is changing the crypto landscape. Learn how and why it matters in our latest post."

def main():
    if not STEEM_USER or not STEEM_POSTING_KEY:
        print("Missing username or posting key.")
        return

    print(f"Using account: {STEEM_USER}")
    print(f"Posting key length: {len(STEEM_POSTING_KEY)}")

    try:
        steem = Steem(keys=[STEEM_POSTING_KEY])
        # Check if account exists
        acc = Account(STEEM_USER, steem_instance=steem)
        print(f"Account found: {acc.name}")
    except Exception as e:
        print(f"Account check failed: {e}")
        return

    trends = ["crypto", "Bitcoin", "Ethereum"]
    topic = random.choice(trends)
    title = f"How {topic} Works"
    body = article(topic)

    print(f"Posting: {title}")
    try:
        steem.post(title, body, author=STEEM_USER, tags=["crypto", "blog"])
        print("Post successful!")
    except Exception as e:
        print(f"Post failed: {e}")

if __name__ == "__main__":
    main()
