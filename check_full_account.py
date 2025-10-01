#!/usr/bin/env python3
"""
Check FULL account details including equity, positions, and sub-accounts
"""

import asyncio
import os
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper
import json

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))


async def check_full_account():
    print('\n' + '='*70)
    print('💰 FULL LIGHTER ACCOUNT DETAILS')
    print('='*70)
    print()
    
    async with LighterAPIWrapper(BASE_URL) as api:
        # Get full account data
        account_data = await api.get_account(ACCOUNT_INDEX)
        
        if not account_data or 'accounts' not in account_data:
            print("❌ Could not fetch account data")
            return
        
        acc = account_data['accounts'][0]
        
        print(f"🔑 Account Index: {acc['index']}")
        print(f"📍 Wallet: {acc['l1_address']}")
        print(f"📊 Status: {'Active' if acc['status'] == 1 else 'Inactive'}")
        print()
        
        print("💰 BALANCES:")
        print("-" * 70)
        
        # Show all balance-related fields
        for key, value in acc.items():
            if 'balance' in key.lower() or 'equity' in key.lower() or 'collateral' in key.lower():
                try:
                    float_val = float(value)
                    print(f"   {key:30s}: ${float_val:,.6f}")
                except:
                    print(f"   {key:30s}: {value}")
        
        print()
        print("📊 POSITION INFO:")
        print("-" * 70)
        
        # Show position-related fields
        for key, value in acc.items():
            if 'position' in key.lower() or 'pnl' in key.lower() or 'margin' in key.lower():
                print(f"   {key:30s}: {value}")
        
        print()
        print("📋 ORDER INFO:")
        print("-" * 70)
        print(f"   Total Orders: {acc.get('total_order_count', 0)}")
        print(f"   Pending Orders: {acc.get('pending_order_count', 0)}")
        print(f"   Isolated Orders: {acc.get('total_isolated_order_count', 0)}")
        
        print()
        print("🗂️  ALL FIELDS:")
        print("-" * 70)
        print(json.dumps(acc, indent=2))
        
        print()
        print("=" * 70)
        print("📝 ANALYSIS:")
        print("=" * 70)
        
        available = float(acc.get('available_balance', 0))
        
        if available < 10:
            print(f"⚠️  Available Balance: ${available:.6f} (too low to trade)")
            print()
            print("💡 Your Total Equity ($103.79) might be:")
            print("   • In open positions (unrealized PnL)")
            print("   • In collateral/margin")
            print("   • In a sub-account")
            print("   • Locked/pending")
            print()
            print("🔍 Check the account fields above to see where the funds are")
        else:
            print(f"✅ Available Balance: ${available:.2f} - Ready to trade!")
        
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(check_full_account())

