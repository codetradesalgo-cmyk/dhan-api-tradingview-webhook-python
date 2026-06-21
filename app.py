import asyncio
import aiohttp
import sqlite3
import uuid
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request, HTTPException
import logging
import os
from dotenv import load_dotenv

# Load real Dhan API keys from the secure environment file
load_dotenv("/opt/codetrades-engine/.env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# --- 1. DETERMINISTIC STATE RECOVERY (The Ledger) ---
def init_db():
    conn = sqlite3.connect("/opt/codetrades-engine/trade_ledger.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS active_trades (transaction_id TEXT PRIMARY KEY, symbol TEXT, status TEXT)")
    conn.commit()
    conn.close()

init_db()

# --- 2. VECTORIZATION (The Memory Cache) ---
class TokenManager:
    def __init__(self):
        logging.info("Initializing NumPy Scrip Master Array...")
        # Simulating the daily CSV load for now
        df = pd.DataFrame({"Symbol": ["NIFTY24000CE", "NIFTY24000PE"], "Token": ["12345", "12346"]})
        self.symbols = df["Symbol"].to_numpy().astype(str)
        self.tokens = df["Token"].to_numpy().astype(str)
        logging.info("NumPy Arrays Loaded. Ready.")

    def get_token(self, symbol: str) -> str:
        idx = np.where(self.symbols == symbol)[0]
        if len(idx) > 0:
            return self.tokens[idx[0]]
        return None

token_manager = TokenManager()

# --- 3. ASYNCHRONOUS API HANDLING (The Execution) ---
async def fire_dhan_order(transaction_id: str, symbol: str, token: str, action: str):
    url = "https://api.dhan.co/orders"
    
    # Securely fetch the API token; avoids hardcoding sensitive data in GitHub
    access_token = os.environ.get("DHAN_ACCESS_TOKEN", "MISSING_TOKEN")
    
    headers = {
        "access-token": access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "correlationId": transaction_id,
        "transactionType": action,
        "exchangeSegment": "NSE_FNO",
        "productType": "MARGIN",
        "orderType": "MARKET",
        "securityId": token,
        "quantity": 25 # 1 Nifty Lot
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    logging.info(f"\033[1;32mFilled {action} for {symbol}. ID: {transaction_id}\033[0m")
                    return "FILLED"
                else:
                    error_data = await response.text()
                    logging.error(f"API Rejected. Status: {response.status}. Reason: {error_data}")
                    return "REJECTED"
        except asyncio.TimeoutError:
            logging.error("Dhan API Timeout. Network dropped packet.")
            return "UNKNOWN"

@app.post("/webhook")
async def webhook_receiver(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed JSON")

    symbol = data.get("symbol")
    action = data.get("action")

    token = token_manager.get_token(symbol)
    if not token:
        raise HTTPException(status_code=404, detail="Strike token not found")

    transaction_id = str(uuid.uuid4())

    conn = sqlite3.connect("/opt/codetrades-engine/trade_ledger.db")
    conn.execute("INSERT INTO active_trades (transaction_id, symbol, status) VALUES (?, ?, ?)", 
                 (transaction_id, symbol, "PENDING"))
    conn.commit()

    final_status = await fire_dhan_order(transaction_id, symbol, token, action)

    conn.execute("UPDATE active_trades SET status = ? WHERE transaction_id = ?", 
                 (final_status, transaction_id))
    conn.commit()
    conn.close()

    return {"status": final_status, "correlation_id": transaction_id}
