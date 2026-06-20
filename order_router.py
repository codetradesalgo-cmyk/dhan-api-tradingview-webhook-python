import os
import requests
import logging

BROKER_API_URL = "https://api.dhan.co/orders"
ACCESS_TOKEN = os.environ.get("BROKER_ACCESS_TOKEN")
CLIENT_ID = os.environ.get("BROKER_CLIENT_ID")

def execute_order(symbol, action, trigger_price, token):
    """
    Converts a Market signal into a dynamic Limit order to prevent slippage.
    """
    # Calculate the Limit offset (0.05% slippage tolerance)
    if action.upper() == "BUY":
        limit_price = round(trigger_price * 1.0005, 2)
        transaction_type = "BUY"
    else:
        limit_price = round(trigger_price * 0.9995, 2)
        transaction_type = "SELL"
        
    headers = {
        "access-token": ACCESS_TOKEN,
        "client-id": CLIENT_ID,
        "Content-Type": "application/json"
    }
    
    # Strict payload formatting to avoid DH-905 errors
    payload = {
        "dhanClientId": CLIENT_ID,
        "transactionType": transaction_type,
        "exchangeSegment": "NSE_FNO",
        "productType": "MARGIN",
        "orderType": "LIMIT",
        "validity": "DAY",
        "securityId": str(token),
        "quantity": 65, # Base lot size multiplier
        "price": limit_price
    }
    
    try:
        # In a real environment, this fires directly to the broker
        # response = requests.post(BROKER_API_URL, headers=headers, json=payload)
        # return response.json()
        
        logging.info(f"Fired {transaction_type} LIMIT for {symbol} at {limit_price}")
        return {"status": "success", "simulated_latency": "22ms"}
        
    except Exception as e:
        logging.error(f"API Routing failed: {str(e)}")
        return {"status": "failed"}