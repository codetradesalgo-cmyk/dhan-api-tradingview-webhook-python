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

1. **Brokerage API:** This engine is strictly hardcoded for Dhan's v2 API structure. 
   👉 [Create your Dhan Account Here to generate your API keys] https://join.dhan.co/?invite=ROCVO41702
2. **Linux VPS:** Provision a clean Ubuntu 22.04+ node. 
   👉 [Deploy an optimized Ubuntu Node Here] https://m.do.co/c/cb6b8162a216
3. **TradingView Premium:** Webhook transmission requires a paid tier. https://in.tradingview.com/?aff_id=167675

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
Payload Structure
Configure your TradingView webhook alerts to transmit strictly formatted JSON.

Endpoint: http://[YOUR_VPS_IP]/webhook

Done-For-You (DFY) Turnkey Deployment
Managing Linux system daemons, configuring Nginx web proxies, and debugging asynchronous worker states can be complex. If one step of the ASGI configuration fails, your webhooks will drop.

If you are a quantitative trader, prop desk, or fund manager who wants to focus purely on strategy logic without managing the backend infrastructure, we offer a Complete DFY Deployment Service.

What is included:

Provisioning of an optimized, low-latency Ubuntu VPS (Mumbai Region).

End-to-end installation of the FastAPI/NumPy routing engine.

Hardening of the Nginx proxy firewall and HTTPS/SSL certification.

Direct integration and testing with your TradingView and Dhan accounts.

Handover of a fully operational, live-market-ready system.

To request a DFY build, visit:
👉 https://topmate.io/codetrades_algo/2159660

Disclaimer
This software is for educational and architectural demonstration purposes. Algorithmic trading carries significant financial risk. The developers are not responsible for capital losses incurred due to misconfigured servers, AWS/broker network outages, or incorrect strategy logic.
