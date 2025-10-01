#!/usr/bin/env python3
"""
Check the last transaction details
"""

import asyncio
from lighter_api_wrapper import LighterAPIWrapper

async def main():
    base_url = "https://mainnet.zklighter.elliot.ai"
    api = LighterAPIWrapper(base_url)
    
    # Last TX hash from logs
    tx_hash = "f509ac227b0652da4136164075d3ae7cc11c66469c3639da0973dde0c250fe616cb4c547ea172509"
    
    print(f"\n🔍 Checking transaction: {tx_hash[:20]}...\n")
    print("="*70)
    
    try:
        # Check if there's an endpoint to get TX status
        async with api.session.get(f"{base_url}/api/v1/transaction/{tx_hash}") as response:
            if response.status == 200:
                data = await response.json()
                print(f"✅ Transaction found!")
                print(f"\n{data}")
            else:
                text = await response.text()
                print(f"❌ HTTP {response.status}: {text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Also check account status
    print("\n" + "="*70)
    print("\n💰 Current Account Status:")
    print("="*70)
    
    account = await api.get_account("281474976667491")
    if account:
        print(f"Available Balance: ${float(account.get('available_balance', 0)) / 1e8:.2f}")
        print(f"Total Order Count: {account.get('total_order_count', 0)}")
        print(f"Open Positions: {len(account.get('open_positions', []))}")
    
    await api.close()

if __name__ == "__main__":
    asyncio.run(main())
