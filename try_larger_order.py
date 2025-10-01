#!/usr/bin/env python3
"""Try with a much larger order size"""

import asyncio
import os
from dotenv import load_dotenv
import lighter
import time

load_dotenv()

async def test_larger():
    """Test with 10x larger order"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print("Testing with MUCH LARGER order")
    print("=" * 70)
    
    try:
        client = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=10
        )
        
        # Try 0.001 BTC instead of 0.0001
        base_amount = 100000  # 0.001 BTC (~$114)
        price = 120000
        
        print(f"Order: 0.001 BTC (~$114 worth)")
        print(f"This is 10x larger than before\n")
        
        order_result, tx_hash, order_id = await client.create_market_order(
            market_index=1,
            client_order_index=int(time.time() * 1000) % 2147483647,
            base_amount=base_amount,
            avg_execution_price=price,
            is_ask=False,
            reduce_only=False
        )
        
        print(f"✅ Order placed: {tx_hash}")
        
        print(f"\n⏳ Waiting 5 seconds...")
        await asyncio.sleep(5)
        
        # Check position
        from lighter_api_wrapper import LighterAPIWrapper
        async with LighterAPIWrapper(base_url) as api:
            account_data = await api.get_account(account_index)
            
            if account_data and 'accounts' in account_data:
                acc = account_data['accounts'][0]
                total_orders = acc.get('total_order_count', 0)
                balance = float(acc.get('available_balance', 0))
                positions = acc.get('positions', [])
                
                print(f"\n📊 Result:")
                print(f"   Total Orders Ever: {total_orders}")
                print(f"   Balance: ${balance:.2f}")
                
                has_position = False
                for pos in positions:
                    size = float(pos.get('size', 0))
                    if size != 0:
                        print(f"   ✅ POSITION EXISTS!")
                        print(f"      Size: {size:.8f}")
                        has_position = True
                
                if not has_position:
                    print(f"   ❌ Still no position")
                
                return total_orders > 0 or has_position
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_larger())
    print(f"\n{'='*70}")
    print(f"SUCCESS!" if result else "STILL FAILED")

