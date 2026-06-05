
import os,json,time,requests
from beem import Steem
from beem.account import Account
from beem.transactionbuilder import TransactionBuilder
from beembase import operations
STEEM_USER=os.getenv("STEEMIT_USERNAME"); STEEM_KEY=os.getenv("STEEMIT_ACTIVE_KEY"); NC_WALLET="0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419"
def post(title,body,tags):
    steem=Steem(keys=[STEEM_KEY])
    steem.post(title,body,author=STEEM_USER,tags=tags)
def swap_steem_to_eth():
    pass
def main():
    try:
        with open("/tmp/trends.json") as f: trends=json.load(f)
    except: trends=["crypto"]
    t=trends[0]
    article=requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        headers={"Authorization":f"Bearer {os.getenv('HF_TOKEN','')}"}, json={"inputs":f"Write a Steemit post about {t}"}).json()[0]["generated_text"]
    if STEEM_USER and STEEM_KEY:
        post(f"How {t} Works",article,["crypto","blog"])
if __name__=="__main__": main()
