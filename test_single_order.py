#!/usr/bin/env python3
"""Test placing a single order to see what happens"""

import asyncio
import os
from dotenv import load_dotenv
import lighter
import time

load_dotenv()

async def test_order():
    """Test placing a single order"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    api_key_index = 10
    
    print("Testing single order placement...")
    print("=" * 70)
    
    try:
        # Initialize client
        client = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=api_key_index
        )
        
        print("✅ Client initialized")
        
        # Order parameters
        market_id = 1  # BTC
        base_amount = 50000  # 0.0005 BTC (~$57 worth)
        current_price = 114000
        exec_price = int(current_price * 1.001)  # 3% slippage
        is_ask = False  # Buy/Long
        client_order_idx = int(time.time() * 1000) % 2147483647
        
        print(f"\n📊 Order Details:")
        print(f"   Market: {market_id} (BTC)")
        print(f"   Size: {base_amount} sats ({base_amount/1e8:.6f} BTC)")
        print(f"   Side: {'SELL/SHORT' if is_ask else 'BUY/LONG'}")
        print(f"   Exec Price: ${exec_price:,}")
        print(f"   Client Order ID: {client_order_idx}")
        
        print(f"\n📤 Placing order...")
        
        # Place order
        order_result, tx_hash, order_id = await client.create_market_order(
            market_index=market_id,
            client_order_index=client_order_idx,
            base_amount=base_amount,
            avg_execution_price=exec_price,
            is_ask=is_ask,
            reduce_only=False
        )
        
        print(f"\n✅ Order Response:")
        print(f"   TX Hash: {tx_hash}")
        print(f"   Order ID: {order_id}")
        print(f"   Result: {order_result}")
        
        # Wait and check position
        print(f"\n⏳ Waiting 5 seconds for order to fill...")
        await asyncio.sleep(5)
        
        # Check account
        from lighter_api_wrapper import LighterAPIWrapper
        async with LighterAPIWrapper(base_url) as api:
            account_data = await api.get_account(account_index)
            
            if account_data and 'accounts' in account_data:
                acc = account_data['accounts'][0]
                balance = float(acc.get('available_balance', 0))
                positions = acc.get('positions', [])
                
                print(f"\n💰 Account Status:")
                print(f"   Balance: ${balance:.2f}")
                print(f"   Open Positions: {len(positions)}")
                
                for i, pos in enumerate(positions, 1):
                    size = float(pos.get('size', 0))
                    if size != 0:
                        print(f"\n   Position {i}:")
                        print(f"      Market: {pos.get('market_id')}")
                        print(f"      Side: {'LONG' if size > 0 else 'SHORT'}")
                        print(f"      Size: {abs(size):.8f}")
                        print(f"      Entry: ${float(pos.get('entry_price', 0)):,.2f}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_order())

