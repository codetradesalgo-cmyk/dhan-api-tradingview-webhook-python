# Dhan API - TradingView Webhook Bridge (Python)

A basic Python/Flask webhook listener to connect TradingView alerts directly to the Dhan HQ API for Indian F&O execution.

## Limitations of this Free Build (Read Before Live Trading)
This repository contains the `lite` execution engine. If you use this script in a live market environment, you will face three structural issues:
1. **The DH-905 Error (Lot Sizing):** This script requires you to hardcode lot sizes. If you accidentally send `60` instead of `65` for Nifty, the exchange will reject the order.
2. **Manual Token Updates:** You must manually find and update the `security_id` (Exchange Token) for the exact strike price you want to trade every single day.
3. **Execution Latency:** Running Flask locally without a production WSGI server causes execution delays of 500ms+, causing massive slippage on fast M1/M5 candles.

## 🚀 The Institutional Blueprint (Sub-50ms Execution)
I engineered a production-grade, zero-touch architecture to solve the friction above. 

The **Smart Routing Engine Blueprint** includes:
* **RAM-Cached Scrip Master:** Automatically maps ATM/OTM strikes dynamically based on Spot price. No manual token updates required.
* **Auto-Lot Sizing Matrix:** Failsafes built-in to auto-correct Nifty (65), BankNifty (30), and Sensex (20) lot parameters.
* **Headless VPS Deployment:** The exact `systemd` and `nginx` configurations to host your engine securely 24/7 on a $5 Ubuntu cloud server.
* **Plug-and-Play TradingView JSONs:** Pre-formatted PineScript payload templates.

**[Download the Full Production-Ready Source Code Here]**(https://topmate.io/codetrades_algo/2159678)

## Setup for Lite Version
1. `pip install -r requirements.txt`
2. Insert your Client ID and Token in `app.py`.
3. Run `python app.py`.