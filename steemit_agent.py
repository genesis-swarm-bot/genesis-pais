import os, json, time, random
from beem import Steem
from beem.account import Account
from supabase import create_client

STEEM_USER = os.getenv("STEEMIT_USERNAME", "genesisai")
STEEM_POSTING_KEY = "5K4Z5JfHh758Put8uc5EtBYmiZ1D8MJxPKJjC3ENERVgJUkti5m"
SUPABASE_URL = "https://jbrcxkrudgwhmqxqtjen.supabase.co"
SUPABASE_KEY = "sb_publishable_LP9aT6_4n7Q3GN_tIXb1vQ_YyV3H1tI"

def log_event(source, title):
    try:
        db = create_client(SUPABASE_URL, SUPABASE_KEY)
        db.table("earnings").insert({
            "source": source,
            "title": title,
            "timestamp": "now()"
        }).execute()
    except Exception as e:
        print(f"Logging failed: {e}")

def article(topic):
    return f"{topic} is changing the crypto landscape. Learn how and why it matters in our latest post."

def main():
    if not STEEM_USER or not STEEM_POSTING_KEY:
        return

    try:
        steem = Steem(keys=[STEEM_POSTING_KEY])
        acc = Account(STEEM_USER, steem_instance=steem)
    except Exception as e:
        print(f"Account error: {e}")
        return

    trends = ["crypto", "Bitcoin", "Ethereum"]
    topic = random.choice(trends)
    title = f"How {topic} Works"
    body = article(topic)

    try:
        steem.post(title, body, author=STEEM_USER, tags=["crypto", "blog"])
        print("Steemit post successful")
        log_event("steemit", title)
    except Exception as e:
        print(f"Post failed: {e}")

if __name__ == "__main__":
    main()
