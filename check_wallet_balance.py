#!/usr/bin/env python3
"""
Check both WALLET balance and LIGHTER balance
"""

import asyncio
import os
from dotenv import load_dotenv
from web3 import Web3
from lighter_api_wrapper import LighterAPIWrapper

load_dotenv()

# Configuration
RPC_URL = os.getenv('RPC_URL', 'https://arb1.arbitrum.io/rpc')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
BASE_URL = os.getenv('LIGHTER_API_URL')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))

# USDC contract on Arbitrum
USDC_ADDRESS = '0xaf88d065e77c8cC2239327C5EDb3A432268e5831'
USDC_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]


async def check_all_balances():
    print('\n' + '='*70)
    print('💰 BALANCE CHECK - WALLET vs LIGHTER EXCHANGE')
    print('='*70)
    print()
    
    # Get wallet address from private key
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = w3.eth.account.from_key(PRIVATE_KEY)
    wallet_address = account.address
    
    print(f"🔑 Your Wallet Address: {wallet_address}")
    print()
    
    # Check ETH balance
    print("1️⃣  ETH Balance (in wallet):")
    try:
        eth_balance_wei = w3.eth.get_balance(wallet_address)
        eth_balance = w3.from_wei(eth_balance_wei, 'ether')
        print(f"   ETH: {eth_balance:.6f} ETH")
        print()
    except Exception as e:
        print(f"   ❌ Could not fetch ETH balance: {e}")
        print()
    
    # Check USDC balance in wallet
    print("2️⃣  USDC Balance (in wallet):")
    try:
        usdc_contract = w3.eth.contract(address=USDC_ADDRESS, abi=USDC_ABI)
        usdc_balance_raw = usdc_contract.functions.balanceOf(wallet_address).call()
        decimals = usdc_contract.functions.decimals().call()
        usdc_balance = usdc_balance_raw / (10 ** decimals)
        print(f"   USDC: ${usdc_balance:.6f}")
        print()
    except Exception as e:
        print(f"   ❌ Could not fetch USDC balance: {e}")
        print()
    
    # Check Lighter balance
    print("3️⃣  Lighter Exchange Balance:")
    async with LighterAPIWrapper(BASE_URL) as api:
        account_data = await api.get_account(ACCOUNT_INDEX)
        if account_data and 'accounts' in account_data and account_data['accounts']:
            acc = account_data['accounts'][0]
            lighter_balance = float(acc['available_balance'])
            print(f"   Lighter: ${lighter_balance:.6f} USDC")
            print()
        else:
            print("   ❌ Could not fetch Lighter balance")
            print()
    
    print('='*70)
    print('📊 SUMMARY:')
    print('='*70)
    try:
        print(f"💵 Total in Wallet: ${usdc_balance:.2f} USDC + {eth_balance:.4f} ETH")
    except:
        print(f"💵 Total in Wallet: Unable to calculate")
    
    try:
        print(f"📈 On Lighter Exchange: ${lighter_balance:.6f} USDC")
    except:
        print(f"📈 On Lighter Exchange: Unable to calculate")
    
    print()
    print('❗ IMPORTANT:')
    print('   • To trade on Lighter, you need USDC on the Lighter exchange')
    print('   • Your wallet balance is separate from your Lighter balance')
    print('   • You must DEPOSIT from wallet → Lighter to trade')
    print('='*70)
    print()


if __name__ == "__main__":
    asyncio.run(check_all_balances())

