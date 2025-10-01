#!/usr/bin/env python3
"""
Test placing a limit order at current market price
"""

import asyncio
import lighter
import os
from dotenv import load_dotenv
import time

load_dotenv()

BASE_URL = os.getenv("LIGHTER_API_URL")
API_KEY_PRIVATE = os.getenv("LIGHTER_API_KEY_PRIVATE")
ACCOUNT_INDEX = int(os.getenv("LIGHTER_ACCOUNT_INDEX"))
API_KEY_INDEX = int(os.getenv("LIGHTER_API_KEY_INDEX"))

async def main():
    print("\n" + "="*70)
    print("🧪 TESTING LIMIT ORDER AT MARKET PRICE")
    print("="*70)
    
    # Initialize client
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    
    # Get orderbook to find best ask
    from lighter_api_wrapper import LighterAPIWrapper
    api = LighterAPIWrapper(BASE_URL)
    
    orderbook = await api.get_orderbook(1)  # BTC market
    
    if orderbook:
        best_ask = orderbook.get('best_ask_price', 0)
        best_bid = orderbook.get('best_bid_price', 0)
        print(f"\n📊 BTC Orderbook:")
        print(f"   Best Ask: ${best_ask}")
        print(f"   Best Bid: ${best_bid}")
        
        # For a long, we buy at the ask price (or slightly above)
        limit_price = best_ask
        
        # Small order size - 0.0001 BTC
        base_amount = 10000  # satoshis
        
        print(f"\n📤 Placing LIMIT BUY order:")
        print(f"   Size: 0.0001 BTC")
        print(f"   Limit Price: ${limit_price}")
        print(f"   (At best ask - should fill immediately)")
        
        try:
            client_order_index = int(time.time() * 1000) % 2147483647
            
            order_result, tx_hash, order_id = await client.create_order(
                market_index=1,
                client_order_index=client_order_index,
                base_amount=base_amount,
                price=int(limit_price),
                is_ask=False,  # Buy
                order_type=lighter.ORDER_TYPE_LIMIT,
                time_in_force=lighter.ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL,
                reduce_only=False
            )
            
            print(f"\n✅ Order placed!")
            print(f"   TX Hash: {tx_hash}")
            print(f"   Order ID: {order_id}")
            print(f"\n⏳ Waiting 3 seconds for execution...")
            await asyncio.sleep(3)
            
            # Check balance
            account = await api.get_account(str(ACCOUNT_INDEX))
            if account:
                balance = float(account.get('available_balance', 0)) / 1e8
                total_orders = account.get('total_order_count', 0)
                positions = len(account.get('open_positions', []))
                
                print(f"\n💰 Account Status:")
                print(f"   Balance: ${balance:.2f}")
                print(f"   Total Orders: {total_orders}")
                print(f"   Positions: {positions}")
                
                if total_orders > 0:
                    print(f"\n🎉 SUCCESS! Order executed!")
                else:
                    print(f"\n❌ Order was accepted but not executed")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    await api.close()
    print("\n" + "="*70)

if __name__ == "__main__":
    asyncio.run(main())

