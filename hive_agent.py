import os, requests, json
from beem import Hive
from beem.account import Account
from beem.transactionbuilder import TransactionBuilder
from beembase import operations
from supabase import create_client

HIVE_ACC = os.getenv("HIVE_ACCOUNT", "genesisai")
HIVE_KEY = os.getenv("HIVE_ACTIVE_KEY", "STM58MZXfEMNrP96vdSapEAXJjW4fhD2poihCL9YcdVZg7iTYpKyw")
NC_WALLET = os.getenv("NC_WALLET_ETH", "0x7c193f13c99f8e420693af5eae0d1a7fdc2a4419")
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

def swap_to_eth(amount_hive):
    r = requests.post("https://api.simpleswap.io/create_exchange", json={
        "fixed": False,
        "currency_from": "HIVE",
        "currency_to": "ETH",
        "amount": amount_hive,
        "address_to": NC_WALLET,
    })
    if r.status_code != 200:
        return
    addr = r.json()["address_from"]
    hive = Hive(keys=[HIVE_KEY])
    acc = Account(HIVE_ACC, hive_instance=hive)
    op = operations.Transfer({"from": HIVE_ACC, "to": addr, "amount": f"{amount_hive:.3f} HIVE", "memo": ""})
    tx = TransactionBuilder(hive_instance=hive)
    tx.appendOps(op)
    tx.appendWif(HIVE_KEY)
    tx.sign()
    tx.broadcast()
    print(f"Swapped {amount_hive} HIVE to ETH")

def main():
    hive = Hive()
    acc = Account(HIVE_ACC, hive_instance=hive)
    hive_bal = float(acc["balance"])
    hbd_bal = float(acc["hbd_balance"])
    total = hive_bal + hbd_bal
    if total > 1:
        swap_to_eth(total)
        log_event("hive", f"Swapped {total:.2f} HIVE/HBD to ETH")

if __name__ == "__main__":
    main()
