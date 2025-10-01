#!/usr/bin/env python3
"""Check current open positions on Lighter"""

import asyncio
import os
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper

load_dotenv()

async def check_positions():
    """Check open positions"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print(f"Checking positions for account: {account_index}")
    print("=" * 70)
    
    async with LighterAPIWrapper(base_url) as api:
        # Get account data
        account_data = await api.get_account(account_index)
        
        if not account_data or 'accounts' not in account_data:
            print("❌ Could not fetch account data")
            return
        
        acc = account_data['accounts'][0]
        
        print(f"\n💰 Account Balance:")
        print(f"   Available: ${float(acc.get('available_balance', 0)):.2f}")
        print(f"   Total: ${float(acc.get('balance', 0)):.2f}")
        
        # Check for open positions
        positions = acc.get('positions', [])
        
        print(f"\n📊 Open Positions: {len(positions)}")
        print("=" * 70)
        
        if not positions:
            print("\n✅ No open positions")
            print("\nℹ️  This means:")
            print("  - The order might not have filled yet")
            print("  - The order might have been rejected")
            print("  - Or it filled and closed very quickly")
        else:
            for i, pos in enumerate(positions, 1):
                market_id = pos.get('market_id', 'Unknown')
                size = float(pos.get('size', 0))
                side = 'LONG' if size > 0 else 'SHORT'
                entry_price = float(pos.get('entry_price', 0))
                unrealized_pnl = float(pos.get('unrealized_pnl', 0))
                
                print(f"\nPosition {i}:")
                print(f"  Market ID: {market_id}")
                print(f"  Side: {side}")
                print(f"  Size: {abs(size):.8f}")
                print(f"  Entry Price: ${entry_price:,.2f}")
                print(f"  Unrealized P&L: ${unrealized_pnl:.2f}")
        
        # Check recent orders
        print(f"\n\n📝 Checking recent orders...")
        print("=" * 70)
        
        import aiohttp
        orders_url = f"{base_url}/api/v1/orders?account_index={account_index}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(orders_url) as response:
                if response.status == 200:
                    orders_data = await response.json()
                    orders = orders_data.get('orders', [])
                    
                    if orders:
                        print(f"\nFound {len(orders)} recent order(s):\n")
                        for order in orders[:5]:  # Show last 5
                            order_id = order.get('order_id', 'N/A')
                            market = order.get('market_id', 'N/A')
                            side = 'BUY' if not order.get('is_ask') else 'SELL'
                            status = order.get('status', 'Unknown')
                            filled = float(order.get('filled_amount', 0))
                            
                            print(f"  Order: {order_id}")
                            print(f"    Market: {market} | {side} | Status: {status}")
                            print(f"    Filled: {filled:.8f}")
                            print()
                    else:
                        print("No recent orders found")
                else:
                    print(f"Could not fetch orders: HTTP {response.status}")

if __name__ == "__main__":
    asyncio.run(check_positions())

