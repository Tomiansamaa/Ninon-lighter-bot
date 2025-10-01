#!/usr/bin/env python3
"""Try a LIMIT order instead of market order"""

import asyncio
import os
from dotenv import load_dotenv
import lighter
import time

load_dotenv()

async def test_limit_order():
    """Test with limit order"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print("Testing LIMIT ORDER (not market)")
    print("=" * 70)
    
    try:
        client = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=10
        )
        
        # Get current price first
        from lighter_api_wrapper import LighterAPIWrapper
        async with LighterAPIWrapper(base_url) as api:
            orderbook_data = await api.get_orderbook(1)
            ob = orderbook_data['order_book_details'][0]
            current_price = float(ob.get('last_trade_price', 114000))
        
        # Place limit order at current price (should fill immediately)
        base_amount = 50000  # 0.0005 BTC
        limit_price = int(current_price * 1.01)  # 1% above market for immediate fill
        
        print(f"Limit Order:")
        print(f"  Size: 0.0005 BTC")
        print(f"  Price: ${limit_price:,} (1% above market)")
        print(f"  Type: LIMIT (0)")
        print(f"  Time in Force: IOC (0)\n")
        
        order_result, tx_hash, order_id = await client.create_order(
            market_index=1,
            client_order_index=int(time.time() * 1000) % 2147483647,
            base_amount=base_amount,
            price=limit_price,
            is_ask=False,  # Buy
            order_type=0,  # LIMIT
            time_in_force=0,  # IMMEDIATE_OR_CANCEL
            reduce_only=False
        )
        
        print(f"✅ Order result: {tx_hash}")
        
        print(f"\n⏳ Waiting 5 seconds...")
        await asyncio.sleep(5)
        
        # Check
        async with LighterAPIWrapper(base_url) as api:
            account_data = await api.get_account(account_index)
            
            if account_data and 'accounts' in account_data:
                acc = account_data['accounts'][0]
                total_orders = acc.get('total_order_count', 0)
                balance = float(acc.get('available_balance', 0))
                
                print(f"\n📊 Result:")
                print(f"   Total Orders: {total_orders}")
                print(f"   Balance: ${balance:.2f}")
                
                positions = acc.get('positions', [])
                for pos in positions:
                    size = float(pos.get('size', 0))
                    if size != 0:
                        print(f"   ✅ POSITION FOUND!")
                        print(f"      Size: {size:.8f}")
                        return True
                
                print(f"   ❌ No position")
                return total_orders > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_limit_order())
    print(f"\n{'='*70}")
    if result:
        print("✅ IT WORKED! Use LIMIT orders, not market orders!")
    else:
        print("❌ Limit orders also don't work")

