#!/usr/bin/env python3
"""Check full account status including permissions"""

import asyncio
import os
from dotenv import load_dotenv
import aiohttp
import json

load_dotenv()

async def check_full_status():
    """Check everything about the account"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print("FULL ACCOUNT STATUS CHECK")
    print("=" * 70)
    print(f"Account Index: {account_index}\n")
    
    async with aiohttp.ClientSession() as session:
        # 1. Get account details
        print("1. ACCOUNT DETAILS:")
        print("-" * 70)
        url = f"{base_url}/api/v1/account?by=index&value={account_index}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if 'accounts' in data and data['accounts']:
                    acc = data['accounts'][0]
                    print(json.dumps(acc, indent=2))
                else:
                    print("No account data")
            else:
                print(f"Error: HTTP {resp.status}")
        
        # 2. Get orderbooks to see market status
        print("\n\n2. MARKET STATUS (BTC):")
        print("-" * 70)
        url = f"{base_url}/api/v1/orderBookDetails?market_id=1"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                if 'order_book_details' in data and data['order_book_details']:
                    ob = data['order_book_details'][0]
                    print(f"Symbol: {ob.get('symbol')}")
                    print(f"Status: {ob.get('status')}")
                    print(f"Min Order Size: {ob.get('min_order_size')}")
                    print(f"Size Increment: {ob.get('size_increment')}")
                    print(f"Price Increment: {ob.get('price_increment')}")
                    print(f"Last Price: ${float(ob.get('last_trade_price', 0)):,.2f}")
                else:
                    print("No orderbook data")
            else:
                print(f"Error: HTTP {resp.status}")
        
        # 3. Try to get recent trades
        print("\n\n3. RECENT TRADES (to see if market is active):")
        print("-" * 70)
        url = f"{base_url}/api/v1/trades?market_id=1&limit=5"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                trades = data.get('trades', [])
                if trades:
                    print(f"Found {len(trades)} recent trades - Market IS active")
                    for t in trades[:3]:
                        print(f"  - ${float(t.get('price', 0)):,.2f} | {t.get('size')} | {t.get('is_buy')}")
                else:
                    print("No recent trades found - Market might be inactive!")
            else:
                print(f"Error: HTTP {resp.status}")
        
        # 4. Check if there are any open orders from us
        print("\n\n4. YOUR ORDERS:")
        print("-" * 70)
        url = f"{base_url}/api/v1/orders?account_index={account_index}&limit=10"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                orders = data.get('orders', [])
                if orders:
                    print(f"Found {len(orders)} order(s):")
                    for order in orders:
                        print(f"\n  Order ID: {order.get('order_id')}")
                        print(f"  Market: {order.get('market_id')}")
                        print(f"  Status: {order.get('status')}")
                        print(f"  Side: {'BUY' if not order.get('is_ask') else 'SELL'}")
                        print(f"  Amount: {order.get('amount')}")
                        print(f"  Filled: {order.get('filled_amount')}")
                else:
                    print("No orders found (even pending ones!)")
            else:
                text = await resp.text()
                print(f"Error: HTTP {resp.status}: {text[:200]}")

if __name__ == "__main__":
    asyncio.run(check_full_status())

