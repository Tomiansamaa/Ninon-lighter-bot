#!/usr/bin/env python3
"""
Check for sub-accounts - the $103 might be there!
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL')
WALLET_ADDRESS = '0xC843b738d7b34c97393e198E6dAA6c4Fb81bdB80'


async def check_all_accounts():
    print('\n' + '='*70)
    print('🔍 SEARCHING FOR YOUR $103 - CHECKING ALL ACCOUNTS')
    print('='*70)
    print()
    
    async with aiohttp.ClientSession() as session:
        # Get ALL accounts for this wallet address
        url = f"{BASE_URL}/api/v1/account?by=l1_address&value={WALLET_ADDRESS}"
        
        print(f"📡 Fetching all accounts for: {WALLET_ADDRESS}")
        print()
        
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                
                if 'accounts' in data and data['accounts']:
                    accounts = data['accounts']
                    print(f"✅ Found {len(accounts)} account(s)!")
                    print()
                    
                    total_equity = 0
                    
                    for i, acc in enumerate(accounts, 1):
                        print(f"{'='*70}")
                        print(f"ACCOUNT #{i}")
                        print(f"{'='*70}")
                        print(f"   Index: {acc.get('index', 'N/A')}")
                        print(f"   Type: {acc.get('account_type', 'N/A')}")
                        print(f"   Name: {acc.get('name', '(no name)')}")
                        print(f"   Status: {'Active' if acc.get('status') == 1 else 'Inactive'}")
                        
                        # Get all balance/equity fields
                        available = float(acc.get('available_balance', 0))
                        collateral = float(acc.get('collateral', 0))
                        total_asset = float(acc.get('total_asset_value', 0))
                        cross_asset = float(acc.get('cross_asset_value', 0))
                        
                        print()
                        print(f"   💰 Available Balance: ${available:,.6f}")
                        print(f"   💰 Collateral: ${collateral:,.6f}")
                        print(f"   💰 Total Asset Value: ${total_asset:,.6f}")
                        print(f"   💰 Cross Asset Value: ${cross_asset:,.6f}")
                        
                        # Check for any other equity/balance fields
                        for key in acc.keys():
                            if 'equity' in key.lower() and key not in ['available_balance', 'collateral', 'total_asset_value', 'cross_asset_value']:
                                try:
                                    val = float(acc[key])
                                    print(f"   💰 {key}: ${val:,.6f}")
                                except:
                                    pass
                        
                        # Count positions
                        positions = acc.get('positions', [])
                        active_positions = [p for p in positions if float(p.get('position', 0)) != 0]
                        
                        if active_positions:
                            print()
                            print(f"   📊 Active Positions: {len(active_positions)}")
                            for pos in active_positions:
                                sym = pos.get('symbol', 'Unknown')
                                size = pos.get('position', 0)
                                value = pos.get('position_value', 0)
                                pnl = pos.get('unrealized_pnl', 0)
                                print(f"      • {sym}: {size} (Value: ${value}, PnL: ${pnl})")
                        
                        total_equity += total_asset
                        print()
                    
                    print(f"{'='*70}")
                    print(f"📊 TOTAL ACROSS ALL ACCOUNTS: ${total_equity:,.2f}")
                    print(f"{'='*70}")
                    print()
                    
                    if abs(total_equity - 103.79) < 1:
                        print("✅ FOUND IT! This matches your $103.79!")
                    elif total_equity < 10:
                        print("⚠️  Total is too low. The $103 might be:")
                        print("   1. In a different wallet entirely")
                        print("   2. The screenshot is from a demo/testnet")
                        print("   3. Cached/old data in the Lighter app")
                        print("   4. In L1 wallet (not deposited to L2 yet)")
                else:
                    print("❌ No accounts found")
            else:
                text = await response.text()
                print(f"❌ API Error {response.status}: {text[:200]}")
    
    print()


if __name__ == "__main__":
    asyncio.run(check_all_accounts())
