#!/usr/bin/env python3
"""
Test script to verify real API data fetching works - FIXED VERSION
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
        signer_client = lighter.SignerClient(
            url=BASE_URL,
            private_key=API_KEY_PRIVATE,
            account_index=ACCOUNT_INDEX,
            api_key_index=API_KEY_INDEX
        )
        print("✅ Signer client initialized\n")
        
        # Create API clients
        print("📦 Creating API clients...")
        # Create ApiClient for making API calls
        api_client = lighter.ApiClient(configuration=lighter.Configuration(host=BASE_URL))
        
        # Create OrderApi and AccountApi
        order_api = lighter.OrderApi(api_client)
        account_api = lighter.AccountApi(api_client)
        print("✅ API clients created\n")
        
        # Test 1: Get available markets
        print("📈 Test 1: Fetching available markets...")
        try:
            orderbooks = await order_api.order_books()
            if isinstance(orderbooks, dict):
                markets = list(orderbooks.keys())
                print(f"✅ Found {len(markets)} markets")
                print(f"   Sample markets: {markets[:10]}")
            elif hasattr(orderbooks, 'order_books'):
                markets = list(orderbooks.order_books.keys())
                print(f"✅ Found {len(markets)} markets")
                print(f"   Sample markets: {markets[:10]}")
            else:
                print(f"✅ Markets data type: {type(orderbooks)}")
                print(f"   Data: {orderbooks}")
            print()
        except Exception as e:
            print(f"❌ Failed to get markets: {e}\n")
            import traceback
            traceback.print_exc()
            return False
        
        # Test 2: Get orderbook for BTC-USD (or first available market)
        test_market = MARKET if MARKET in markets else markets[0] if markets else 'BTC-USD'
        print(f"📊 Test 2: Fetching orderbook for {test_market}...")
        try:
            orderbook = await order_api.order_book_details(test_market)
            
            if orderbook:
                # Try different field names
                bids = None
                asks = None
                
                if isinstance(orderbook, dict):
                    bids = orderbook.get('bids', [])
                    asks = orderbook.get('asks', [])
                elif hasattr(orderbook, 'bids') and hasattr(orderbook, 'asks'):
                    bids = orderbook.bids
                    asks = orderbook.asks
                
                print(f"✅ Orderbook received")
                print(f"   Type: {type(orderbook)}")
                
                if bids and asks:
                    print(f"   Bids: {len(bids)} orders")
                    print(f"   Asks: {len(asks)} orders")
                    
                    # Try to get price
                    try:
                        if isinstance(bids[0], (list, tuple)):
                            best_bid = float(bids[0][0])
                            best_ask = float(asks[0][0])
                        else:
                            best_bid = float(bids[0].price if hasattr(bids[0], 'price') else bids[0])
                            best_ask = float(asks[0].price if hasattr(asks[0], 'price') else asks[0])
                        
                        mid_price = (best_bid + best_ask) / 2
                        
                        print(f"   Best Bid: ${best_bid:,.2f}")
                        print(f"   Best Ask: ${best_ask:,.2f}")
                        print(f"   Mid Price: ${mid_price:,.2f}")
                    except Exception as parse_error:
                        print(f"   Could not parse prices: {parse_error}")
                        print(f"   Bid sample: {bids[0] if bids else 'N/A'}")
                        print(f"   Ask sample: {asks[0] if asks else 'N/A'}")
                else:
                    print(f"   Could not find bids/asks")
                    print(f"   Orderbook attributes: {dir(orderbook) if hasattr(orderbook, '__dict__') else 'N/A'}")
                print()
            else:
                print(f"❌ No orderbook data received\n")
                
        except Exception as e:
            print(f"❌ Failed to get orderbook: {e}\n")
            import traceback
            traceback.print_exc()
        
        # Test 3: Get account balance
        print(f"💰 Test 3: Fetching account balance...")
        try:
            account = await account_api.account(account_index=ACCOUNT_INDEX)
            
            print(f"✅ Account data received")
            print(f"   Type: {type(account)}")
            
            # Try to extract balance
            if isinstance(account, dict):
                print(f"   Raw data: {account}")
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
                    print(f"   Available fields: {list(account.keys())}")
            elif hasattr(account, '__dict__'):
                print(f"   Account attributes: {', '.join([a for a in dir(account) if not a.startswith('_')])}")
                # Try common balance attributes
                for attr in ['balance', 'available_balance', 'free_balance', 'equity', 'total_balance']:
                    if hasattr(account, attr):
                        bal = getattr(account, attr)
                        print(f"   {attr}: ${float(bal):,.2f}")
                        break
            print()
                
        except Exception as e:
            print(f"❌ Failed to get account balance: {e}\n")
            import traceback
            traceback.print_exc()
        
        # Cleanup
        await api_client.close()
        await signer_client.close()
        
        # Summary
        print("=" * 70)
        print("✅ TESTS COMPLETED!")
        print("=" * 70)
        print()
        print("📝 Next steps:")
        print("   1. Review the output above")
        print("   2. Update the strategy code to use correct field names")
        print("   3. Enable live trading if tests passed")
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

