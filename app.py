from flask import Flask, request, jsonify
from dhanhq import dhanhq

app = Flask(__name__)

# NOTE: Free version requires hardcoded API credentials.
# The Institutional Blueprint uses secure .env routing.
CLIENT_ID = "YOUR_CLIENT_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

dhan = dhanhq(CLIENT_ID, ACCESS_TOKEN)

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    try:
        # ⚠️ UNOPTIMIZED ROUTING
        # Free version does not utilize RAM-cached Scrip Masters.
        # You must manually map and update the exact token for every strike price daily.
        payload = request.json
        
        sec_id = payload.get("security_id") # Must be exact exchange token (e.g., '42315' for Nifty PE)
        action = payload.get("action")      # 'BUY' or 'SELL'
        qty = int(payload.get("quantity"))  # Must manually match exact NSE lot multiples or will throw DH-905
        
        print(f"Received webhook: {action} {qty} qty of token {sec_id}")

        # Basic execution wrapper (Latencies > 500ms expected locally)
        order = dhan.place_order(
            security_id=sec_id,
            exchange_segment='NSE_FNO',
            transaction_type=action,
            quantity=qty,
            order_type='MARKET',
            product_type='MARGIN',
            price=0
        )
        
        print(f"Exchange Response: {order}")
        return jsonify({"status": "sent", "response": order}), 200

    except Exception as e:
        print(f"Order Failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    # Free version runs on local dev server. It will crash if your PC sleeps.
    app.run(host='0.0.0.0', port=5000)