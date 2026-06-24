# Asynchronous Webhook Engine for Dhan API 

An institutional-grade, sub-50ms execution engine designed to route TradingView webhooks directly to the Dhan API. 

Standard retail architectures built on synchronous frameworks (Flask/Django) suffer from severe input/output blocking, resulting in multi-second slippage during high-volatility market opens. This repository bypasses the WSGI bottleneck entirely by utilizing a pure ASGI framework, enabling true concurrent execution for quantitative strategies.

## Architectural Advantages

* **Concurrent I/O (FastAPI + Uvicorn):** Processes simultaneous webhook payloads asynchronously. If 10 TradingView alerts fire at the exact same millisecond, 0 are queued.
* **Vectorized O(1) Token Caching:** Eliminates database latency. Contract master lists are loaded directly into server RAM as NumPy arrays, allowing instantaneous script-to-token lookups.
* **Deterministic State Recovery:** SQLite implementation prevents duplicate order execution and handles broker-side network timeouts cleanly.
* **Hardened Security:** API credentials are intentionally stripped from the application layer and called dynamically from isolated kernel environments.

## Prerequisite Infrastructure

To deploy this engine without network latency, you cannot run it locally on a Windows machine. You must provision an Ubuntu server located near the NSE exchange servers.

1. **Brokerage API:** This engine is strictly mapped to Dhan's v2 API structure. You must have active production API credentials.
2. **Linux VPS:** Provision a clean Ubuntu 22.04+ node. 
3. **TradingView Premium:** Unrestricted, high-frequency webhook transmission requires a paid TradingView tier.

---

## ⚠️ Deploying to Live F&O Markets?

The open-source engine below handles baseline asynchronous routing. However, to execute Nifty, BankNifty, or MCX options, you must inject dynamic exchange `securityId` tokens into your JSON payloads. 

Parsing the 100MB+ Dhan daily master CSV during live market hours will introduce heavy CPU bottlenecks and cause severe execution slippage. Furthermore, hardcoding your expiry dates will break your execution engine when the exchange shifts expiry schedules (e.g., the recent Nifty shift to Tuesdays).

For quants moving to live capital, we have packaged the production-ready options routing layer:

📦 **[Premium Module: Dynamic F&O Token Mapper & Strike Resolver] https://topmate.io/codetrades_algo/2170763**
* **$O(1)$ Lookup Latency:** Achieves sub-microsecond token mapping via pure Python local memory caching. Bypasses Pandas bloat entirely.
* **Auto-Expiry Discovery:** Automatically parses the exchange master to find the nearest valid weekly expiries (maintenance-free rollovers).
* **Dynamic Strike Resolver:** Mathematically converts live spot prices into valid exchange ATM/OTM strikes instantly for multiple indices.

---

## Core Deployment 

Once your Ubuntu node is live, run the following commands to construct the environment and ignite the engine.

```bash
# Clone the repository
git clone [https://github.com/codetradesalgo-cmyk/dhan-api-tradingview-webhook-python.git](https://github.com/codetradesalgo-cmyk/dhan-api-tradingview-webhook-python.git) /opt/codetrades-engine
cd /opt/codetrades-engine

# Build the isolated environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Inject secure credentials
echo 'DHAN_ACCESS_TOKEN="your_production_token_here"' > .env

# Ignite the ASGI workers
uvicorn app:app --host 0.0.0.0 --port 80 --workers 3
```

## Payload Structure

​Configure your TradingView webhook alerts to transmit strictly formatted JSON.
​Endpoint: http://[YOUR_VPS_IP]/webhook

## ​Disclaimer

​This software is for educational and architectural demonstration purposes. Algorithmic trading carries significant financial risk. The developers are not responsible for capital losses incurred due to misconfigured servers, AWS/broker network outages, or incorrect strategy logic.
