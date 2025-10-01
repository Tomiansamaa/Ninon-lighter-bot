#!/usr/bin/env python3
"""
Check your actual Lighter account balance
"""

import asyncio
import os
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))


async def show_balance():
    async with LighterAPIWrapper(BASE_URL) as api:
        account = await api.get_account(ACCOUNT_INDEX)
        if account and 'accounts' in account and account['accounts']:
            acc = account['accounts'][0]
            balance = float(acc['available_balance'])
            
            print('\n' + '='*70)
            print('💰 YOUR LIGHTER ACCOUNT BALANCE')
            print('='*70)
            print(f"Account Index: {acc['index']}")
            print(f"Wallet Address: {acc['l1_address']}")
            print(f"Available Balance: ${balance:.6f} USDC")
            print(f"Status: {'Active' if acc['status'] == 1 else 'Inactive'}")
            print(f"Total Orders Ever: {acc['total_order_count']}")
            print('='*70)
            print()
            
            if balance < 10:
                print('🚨 WARNING: Balance too low to trade!')
                print(f'   Your balance: ${balance:.6f}')
                print('   Minimum order size: $10-20 depending on market')
                print()
                print('📝 To trade, you need to:')
                print('   1. Deposit USDC to Lighter from your wallet')
                print('   2. Use the Lighter web app or SDK to deposit')
                print('   3. Wait for deposit confirmation')
                print()
                return False
            else:
                print(f'✅ You have ${balance:.2f} USDC available')
                print('   This is enough to start trading!')
                return True
        else:
            print('❌ Could not fetch account data')
            return False


if __name__ == "__main__":
    can_trade = asyncio.run(show_balance())
    exit(0 if can_trade else 1)

