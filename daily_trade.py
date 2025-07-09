#!/usr/bin/env python3

import os
import ccxt
import sys

def main():
    # 1. Load credentials from environment variables
    api_key = os.getenv("KRAKEN_TRADE_API_KEY")
    api_secret = os.getenv("KRAKEN_TRADE_API_SECRET")
    if not api_key or not api_secret:
        print("Error: Trade API credentials not found in environment.")
        sys.exit(1)

    # 2. Connect to Kraken using ccxt
    kraken = ccxt.kraken({
        'apiKey': api_key,
        'secret': api_secret,
    })

    # 3. Define the trading parameters
    symbol = 'BTC/USD'        # the trading pair (adjust if needed)
    amount = 0.00012          # how many BTC to buy
    order_type = 'market'     # using a market order

    # 4. Place the market buy order
    try:
        print(f"Placing {order_type} buy order for {amount} BTC on {symbol}...")
        order = kraken.create_order(symbol, order_type, 'buy', amount)
        print("Order placed successfully:")
        print(order)
    except Exception as e:
        print(f"Error placing order: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
