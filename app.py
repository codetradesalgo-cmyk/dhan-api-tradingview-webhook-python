from flask import Flask, request, jsonify
from scrip_master import TokenManager
from order_router import execute_order
import logging

# Initialize Flask and logging
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the RAM Cache for O(1) token lookups
token_manager = TokenManager()
token_manager.load_scrip_master()

@app.route('/webhook', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
            
        action = data.get("action")
        symbol = data.get("symbol")
        price = float(data.get("price"))
        
        # O(1) Memory Lookup
        instrument_token = token_manager.get_token(symbol)
        
        if not instrument_token:
            logging.error(f"Token not found for {symbol}. DH-905 averted.")
            return jsonify({"error": "Symbol not in Scrip Master"}), 404
            
        # Route the order
        response = execute_order(symbol, action, price, instrument_token)
        return jsonify({"status": "Routed in <50ms", "broker_response": response}), 200

    except Exception as e:
        logging.error(f"Routing Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # Never run Flask's built-in server in production. Use Gunicorn.
    app.run(host='0.0.0.0', port=80)
