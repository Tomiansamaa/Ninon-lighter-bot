#!/usr/bin/env python3
"""
Simple test to place a SHORT market order on BTC with 50x leverage
"""
import asyncio
import lighter
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', '10'))

async def get_current_btc_price():
    """Get current BTC price from Lighter API"""
    from lighter_api_wrapper import LighterAPIWrapper
    wrapper = LighterAPIWrapper(BASE_URL)
    
    # Get BTC orderbook
    orderbook = await wrapper.get_orderbook(1)  # market_id=1 for BTC
    await wrapper.close()
    
    if orderbook and 'order_book_details' in orderbook:
        btc_data = orderbook['order_book_details'][0]
        last_price = float(btc_data['last_trade_price'])
        print(f"📊 BTC Last Trade Price: ${last_price:,.2f}")
        return last_price
    else:
        print(f"❌ Failed to get BTC price: {orderbook}")
        return None

async def place_long_order():
    """Place a LONG market order on BTC"""
    
    print("=" * 70)
    print("🟢 PLACING LONG ORDER TEST")
    print("=" * 70)
    print(f"Account Index: {ACCOUNT_INDEX}")
    print(f"API Key Index: {API_KEY_INDEX}")
    print(f"Market: BTC (index 1)")
    print(f"Side: LONG (buy)")
    print(f"Leverage: 50x")
    print(f"Slippage: 0.1%")
    print()
    
    # Initialize Lighter client
    print("🔑 Initializing Lighter client...")
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    print("✅ Client initialized")
    print()
    
    # Get current BTC price
    current_price = await get_current_btc_price()
    if not current_price:
        print("❌ Cannot proceed without price")
        return
    print()
    
    # Calculate order parameters
    # For a LONG, we want to BUY (is_ask=False)
    # Position size: 0.0002 BTC (~$23 at current price, with 50x = ~$1150 exposure)
    position_size_btc = 0.0002  # Small test size
    base_amount = int(position_size_btc * 1e8)  # Convert to satoshis
    
    # For slippage 0.1%, for a LONG (buy), we're willing to buy at 0.1% above current price
    slippage = 0.001  # 0.1%
    avg_execution_price = int(current_price * (1 + slippage))
    
    # Generate unique client order index
    client_order_index = int(time.time() * 1000) % 2147483647
    
    print("📋 Order Parameters:")
    print(f"   Position Size: {position_size_btc} BTC = {base_amount} satoshis")
    print(f"   Current Price: ${current_price:,.2f}")
    print(f"   Avg Execution Price: ${avg_execution_price:,} (with 0.1% slippage)")
    print(f"   is_ask: False (LONG/BUY)")
    print(f"   reduce_only: False")
    print(f"   client_order_index: {client_order_index}")
    print()
    
    # Place the order
    try:
        print("📤 Placing LONG market order...")
        order_result, tx_hash, order_id = await client.create_market_order(
            market_index=1,  # BTC
            client_order_index=client_order_index,
            base_amount=base_amount,
            avg_execution_price=avg_execution_price,
            is_ask=False,  # LONG = BUY
            reduce_only=False
        )
        
        print()
        print("=" * 70)
        print("✅ ORDER SUBMITTED")
        print("=" * 70)
        print(f"TX Hash: {tx_hash}")
        print(f"Order ID: {order_id}")
        print(f"Order Result: {order_result}")
        print()
        
        # Wait a bit then check if it filled
        print("⏳ Waiting 5 seconds to check if order filled...")
        await asyncio.sleep(5)
        
        # Check account status
        print()
        print("📊 Checking account status...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{BASE_URL}/api/v1/account"
            params = {
                'by': 'index',
                'value': str(ACCOUNT_INDEX)
            }
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   Total Orders: {data.get('total_order_count', 0)}")
                    print(f"   Pending Orders: {data.get('pending_order_count', 0)}")
                    print(f"   Available Balance: ${data.get('available_balance', '0')}")
                    
                    positions = data.get('positions', [])
                    print(f"   Positions: {len(positions)}")
                    for pos in positions:
                        if pos.get('symbol') == 'BTC':
                            print(f"      BTC Position: {pos.get('position', '0')} BTC")
                            print(f"      Entry Price: ${pos.get('avg_entry_price', '0')}")
                            print(f"      Unrealized P&L: ${pos.get('unrealized_pnl', '0')}")
                else:
                    print(f"   ❌ Failed to get account: HTTP {response.status}")
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ORDER FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(place_long_order())
