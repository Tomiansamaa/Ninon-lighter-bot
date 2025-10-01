#!/usr/bin/env python3
"""Test using create_order with explicit ORDER_TYPE_MARKET"""

import asyncio
import os
from dotenv import load_dotenv
import lighter
import time

load_dotenv()

async def test_explicit_market_order():
    """Test with explicit order type"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print("Testing with explicit ORDER_TYPE_MARKET")
    print("=" * 70)
    
    try:
        client = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=10
        )
        
        print("✅ Client initialized")
        
        # Order parameters
        market_id = 1
        client_order_idx = int(time.time() * 1000) % 2147483647
        base_amount = 20000  # 0.0002 BTC
        price = 120000  # High price for market buy
        is_ask = False  # Buy
        
        print(f"\n📊 Order Parameters:")
        print(f"   Market: {market_id}")
        print(f"   Client Order ID: {client_order_idx}")
        print(f"   Base Amount: {base_amount} sats")
        print(f"   Price: ${price}")
        print(f"   Side: {'SELL' if is_ask else 'BUY'}")
        print(f"   Order Type: MARKET (1)")
        print(f"   Time in Force: IOC (0)")
        
        # Use create_order with explicit parameters
        print(f"\n📤 Placing order with create_order()...")
        
        order_result, tx_hash, order_id = await client.create_order(
            market_index=market_id,
            client_order_index=client_order_idx,
            base_amount=base_amount,
            price=price,
            is_ask=is_ask,
            order_type=1,  # ORDER_TYPE_MARKET
            time_in_force=0,  # ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL
            reduce_only=False
        )
        
        print(f"\n✅ Order Response:")
        print(f"   TX Hash: {tx_hash}")
        print(f"   Order ID: {order_id}")
        
        # Wait and check
        print(f"\n⏳ Waiting 5 seconds...")
        await asyncio.sleep(5)
        
        from lighter_api_wrapper import LighterAPIWrapper
        async with LighterAPIWrapper(base_url) as api:
            account_data = await api.get_account(account_index)
            
            if account_data and 'accounts' in account_data:
                acc = account_data['accounts'][0]
                balance = float(acc.get('available_balance', 0))
                positions = acc.get('positions', [])
                
                print(f"\n💰 Result:")
                print(f"   Balance: ${balance:.2f}")
                print(f"   Positions: {len(positions)}")
                
                for pos in positions:
                    size = float(pos.get('size', 0))
                    if size != 0:
                        print(f"   ✅ POSITION FOUND!")
                        print(f"      Market: {pos.get('market_id')}")
                        print(f"      Size: {size:.8f}")
                        print(f"      Entry: ${float(pos.get('entry_price', 0)):,.2f}")
                        return True
                
                print(f"   ❌ Still no position")
                return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_explicit_market_order())
    print(f"\n{'='*70}")
    print(f"Result: {'SUCCESS' if result else 'FAILED'}")
    print(f"{'='*70}")

