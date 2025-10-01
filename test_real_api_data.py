#!/usr/bin/env python3
"""
Test script to verify real API data fetching works
"""

import lighter
import asyncio
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configuration
BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', 2))
MARKET = 'BTC-USD'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_real_data():
    """Test fetching real data from Lighter API"""
    print("\n" + "=" * 70)
    print("🧪 TESTING REAL API DATA INTEGRATION")
    print("=" * 70)
    print()
    
    try:
        # Initialize Lighter client
        print("🔑 Initializing Lighter client...")
        client = lighter.SignerClient(
            url=BASE_URL,
            private_key=API_KEY_PRIVATE,
            account_index=ACCOUNT_INDEX,
            api_key_index=API_KEY_INDEX
        )
        print("✅ Client initialized\n")
        
        # Test 1: Get available markets
        print("📈 Test 1: Fetching available markets...")
        try:
            orderbooks = await client.order_api.order_books()
            if isinstance(orderbooks, dict):
                markets = list(orderbooks.keys())
                print(f"✅ Found {len(markets)} markets")
                print(f"   Sample markets: {markets[:10]}")
            else:
                print(f"✅ Markets data: {orderbooks}")
            print()
        except Exception as e:
            print(f"❌ Failed to get markets: {e}\n")
            return False
        
        # Test 2: Get orderbook for BTC-USD
        print(f"📊 Test 2: Fetching orderbook for {MARKET}...")
        try:
            orderbook = await client.order_api.order_book_details(MARKET)
            
            if orderbook:
                bids = orderbook.get('bids', [])
                asks = orderbook.get('asks', [])
                
                print(f"✅ Orderbook received")
                print(f"   Bids: {len(bids)} orders")
                print(f"   Asks: {len(asks)} orders")
                
                if bids and asks:
                    best_bid = float(bids[0][0])
                    best_ask = float(asks[0][0])
                    mid_price = (best_bid + best_ask) / 2
                    
                    print(f"   Best Bid: ${best_bid:,.2f}")
                    print(f"   Best Ask: ${best_ask:,.2f}")
                    print(f"   Mid Price: ${mid_price:,.2f}")
                    print()
                else:
                    print("⚠️  Orderbook has no bids or asks\n")
            else:
                print(f"❌ No orderbook data received\n")
                return False
                
        except Exception as e:
            print(f"❌ Failed to get orderbook: {e}\n")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 3: Get account balance
        print(f"💰 Test 3: Fetching account balance...")
        try:
            account = await client.account_api.account(account_index=ACCOUNT_INDEX)
            
            print(f"✅ Account data received")
            print(f"   Raw data: {account}")
            
            # Try to extract balance
            if isinstance(account, dict):
                balance = (
                    account.get('balance') or
                    account.get('available_balance') or
                    account.get('free_balance') or
                    account.get('equity') or
                    account.get('total_balance')
                )
                
                if balance is not None:
                    print(f"   Balance: ${float(balance):,.2f}")
                else:
                    print(f"⚠️  Could not find balance field")
                    print(f"   Available fields: {list(account.keys())}")
            print()
                
        except Exception as e:
            print(f"❌ Failed to get account balance: {e}\n")
            import traceback
            traceback.print_exc()
            return False
        
        # Summary
        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print()
        print("📝 Real API integration is working!")
        print("   ✅ Can fetch market data")
        print("   ✅ Can fetch orderbook prices")
        print("   ✅ Can fetch account data")
        print()
        print("⚠️  Next step: Enable live trading in aggressive_bot_config.py")
        print("   Set TRADING_ENABLED = True")
        print()
        return True
        
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_real_data())
    exit(0 if success else 1)

