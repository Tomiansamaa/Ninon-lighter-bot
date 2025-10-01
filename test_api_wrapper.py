#!/usr/bin/env python3
"""
Test the lightweight API wrapper
"""

import asyncio
import os
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))
MARKET_ID = 1  # BTC-USD is typically market_id 1, we'll discover from markets list


async def test_wrapper():
    print("\n" + "=" * 70)
    print("🧪 TESTING LIGHTWEIGHT API WRAPPER")
    print("=" * 70)
    print()
    
    async with LighterAPIWrapper(BASE_URL) as api:
        # Test 1: Get markets
        print("📈 Test 1: Getting markets...")
        markets_data = await api.get_markets()
        market_id_to_test = MARKET_ID
        
        if markets_data:
            print(f"✅ Markets data received")
            print(f"   Type: {type(markets_data)}")
            print(f"   Keys: {list(markets_data.keys()) if isinstance(markets_data, dict) else 'N/A'}")
            
            if 'order_books' in markets_data:
                order_books = markets_data['order_books']
                print(f"   Found {len(order_books)} markets")
                if order_books:
                    print(f"   First market sample: {order_books[0]}")
                    # Get first market_id for testing
                    if 'market_id' in order_books[0]:
                        market_id_to_test = order_books[0]['market_id']
        else:
            print("⚠️  Could not get markets")
        print()
        
        # Test 2: Get orderbook
        print(f"📊 Test 2: Getting orderbook for market_id={market_id_to_test}...")
        orderbook = await api.get_orderbook(market_id_to_test)
        if orderbook:
            print(f"✅ Orderbook received")
            print(f"   Keys: {list(orderbook.keys())}")
            
            # Try to extract price
            if 'bids' in orderbook and 'asks' in orderbook:
                bids = orderbook['bids']
                asks = orderbook['asks']
                print(f"   Bids: {len(bids)} | Asks: {len(asks)}")
                
                if bids and asks:
                    best_bid = float(bids[0]['price']) if isinstance(bids[0], dict) else float(bids[0][0])
                    best_ask = float(asks[0]['price']) if isinstance(asks[0], dict) else float(asks[0][0])
                    mid_price = (best_bid + best_ask) / 2
                    print(f"   Best Bid: ${best_bid:,.2f}")
                    print(f"   Best Ask: ${best_ask:,.2f}")
                    print(f"   Mid Price: ${mid_price:,.2f}")
            else:
                print(f"   Sample data: {str(orderbook)[:200]}")
        else:
            print("⚠️  Could not get orderbook")
        print()
        
        # Test 3: Get account
        print(f"💰 Test 3: Getting account {ACCOUNT_INDEX}...")
        account = await api.get_account(ACCOUNT_INDEX)
        if account:
            print(f"✅ Account data received")
            print(f"   Keys: {list(account.keys())}")
            
            # Try to find balance
            for key in ['balance', 'available_balance', 'free_balance', 'equity', 'total_balance']:
                if key in account:
                    print(f"   {key}: ${float(account[key]):,.2f}")
                    break
            else:
                print(f"   Sample data: {str(account)[:300]}")
        else:
            print("⚠️  Could not get account")
        print()
        
        print("=" * 70)
        print("✅ WRAPPER TEST COMPLETE!")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_wrapper())
