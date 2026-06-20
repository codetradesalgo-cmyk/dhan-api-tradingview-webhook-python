# ⚡ Indian F&O Webhook Bridge (Sub-50ms Execution)

A localized Python Flask middleware engine utilizing a Pandas RAM-cache to eliminate TradingView webhook latency and prevent `DH-905` lot-size rejection errors in the Indian F&O market.

**Why this exists:** Routing direct TradingView webhooks to Indian broker APIs introduces 1,500ms+ of queuing latency. On a fast Nifty breakout, crossing the bid-ask spread with a 2-second delay guarantees massive slippage. Furthermore, direct webhooks fail because broker APIs require strict, static `SEM_LOT_SIZE` multipliers and exchange tokens, not dynamic PineScript data.

This architecture intercepts the dynamic JSON payload, performs an instant `O(1)` memory lookup in Pandas to extract the exact static token, and fires a limit order to the broker in under 50ms.

---

## 🛠️ Mandatory Prerequisites (Infrastructure)

To run this middleware securely without dropouts, you must deploy it on a dedicated, low-latency Linux server and utilize an API-friendly broker. Do not run this on your local Windows machine. 

1. **The Server (VPS):** Deploy a headless Ubuntu Droplet.
   👉 [Spin up your Ubuntu VPS here (DigitalOcean)] -> https://m.do.co/c/cb6b8162a216
2. **The Broker API:** This bridge is optimized for brokers with high-frequency API rate limits.
   👉 [Open an API-enabled Dhan Account] -> https://join.dhan.co/?invite=ROCVO41702
3. **TradingView Webhooks** This bridge is optimized for signals generated from TradingView Alerts
   👉 [Unlock High-Frequency Webhooks on TradingView Here] -> https://in.tradingview.com/?aff_id=167675
---

## 🏗️ Core Architecture Overview

1. `app.py` (Flask Server): Listens for incoming TradingView webhooks on Port 80.
2. `scrip_master.py` (Pandas Engine): Downloads the daily NSE Scrip Master CSV on boot.
3. `order_router.py`: Calculates dynamic limit offsets (e.g., LTP + 0.05%) to cap slippage.

---

## 🚀 Deployment Instructions (DIY)

*Warning: You must have a basic understanding of Linux command-line interfaces, SSH, and Python virtual environments to deploy this securely.*

1. SSH into your Ubuntu VPS.
2. Update dependencies: `sudo apt update && sudo apt install python3-pip python3-venv -y`
3. Clone this repository: `git clone https://github.com/YourUsername/fno-webhook-bridge.git`
4. Set up the virtual environment: `python3 -m venv venv && source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`
6. Add your Broker API Keys to the `.env` file.
7. Configure `gunicorn` and set up the `systemd` background service to ensure the bridge stays alive 24/7.

---

## 🛑 Need Help? (Done-For-You Setup)

If you are a trader, not a Linux sysadmin, misconfiguring the `systemd` service or the WSGI environment will result in dropped webhooks and missed trades.

If you want to skip the command line and have this institutional architecture built for you, I offer a **1-on-1 Remote Deployment Service**. I will provision the server, lock down the firewalls, and build the exact sub-50ms bridge end-to-end.

👉 [Book the Done-For-You VPS Integration Here] -> https://topmate.io/codetrades_algo/2159660
👉 [Book the Architecture & API Consultation Here] -> https://topmate.io/codetrades_algo/2164632
