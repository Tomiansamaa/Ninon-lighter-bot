#!/usr/bin/env python3
"""
Find your Lighter account index
This must be done before initializing the trading bot
"""

import requests
import os
from dotenv import load_dotenv
from eth_account import Account

# Load environment variables
load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
ETH_PRIVATE_KEY = os.getenv('PRIVATE_KEY')

def get_l1_address():
    """Get the L1 address from private key"""
    if not ETH_PRIVATE_KEY:
        print("❌ PRIVATE_KEY not found in .env")
        return None
    
    try:
        account = Account.from_key(ETH_PRIVATE_KEY)
        return account.address
    except Exception as e:
        print(f"❌ Error getting address: {e}")
        return None

def find_account_index(l1_address):
    """Find account index for an L1 address"""
    print(f"🔍 Looking up account index for: {l1_address}\n")
    
    # Try to get account by L1 address
    url = f"{BASE_URL}/api/v1/accountByL1Address"
    params = {"l1_address": l1_address}
    
    try:
        response = requests.get(url, params=params)
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Account found!")
            print(f"\nResponse: {data}\n")
            
            if 'account_index' in data:
                account_index = data['account_index']
                print(f"🎯 Your ACCOUNT_INDEX is: {account_index}")
                print(f"\n📝 Update your .env file:")
                print(f"   LIGHTER_ACCOUNT_INDEX={account_index}\n")
                return account_index
            else:
                print("⚠️  Account data found but no account_index field")
                print(f"   Full response: {data}")
                return None
        else:
            print(f"⚠️  API returned status {response.status_code}")
            print(f"   Response: {response.text}\n")
            
            if response.status_code == 404:
                print("💡 This means:")
                print("   • Your account doesn't exist in Lighter yet")
                print("   • You need to create an account first")
                print("   • Visit https://lighter.xyz and connect your wallet")
                print("   • Or use the Lighter SDK to create an account\n")
            
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def try_all_accounts(l1_address):
    """Try to find all accounts associated with L1 address"""
    print(f"\n🔍 Searching for all accounts linked to {l1_address}...\n")
    
    url = f"{BASE_URL}/api/v1/accountsByL1Address"
    params = {"l1_address": l1_address}
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Accounts found!")
            print(f"\nResponse: {data}\n")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"📊 Found {len(data)} account(s):")
                for i, account in enumerate(data, 1):
                    print(f"\n   Account {i}:")
                    if 'account_index' in account:
                        print(f"      Index: {account['account_index']}")
                    print(f"      Data: {account}")
                
                if 'account_index' in data[0]:
                    print(f"\n🎯 Use this as your ACCOUNT_INDEX: {data[0]['account_index']}\n")
                    return data[0]['account_index']
            else:
                print("⚠️  No accounts found in response")
            
            return None
        else:
            print(f"⚠️  API returned status {response.status_code}")
            print(f"   Response: {response.text}\n")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 70)
    print("🔍 LIGHTER ACCOUNT INDEX FINDER")
    print("=" * 70)
    print()
    
    # Get L1 address
    l1_address = get_l1_address()
    
    if not l1_address:
        return
    
    print(f"📍 Your Wallet Address: {l1_address}\n")
    
    # Try to find account index
    account_index = find_account_index(l1_address)
    
    if account_index is None:
        # Try alternative endpoint
        account_index = try_all_accounts(l1_address)
    
    if account_index is None:
        print("=" * 70)
        print("⚠️  ACCOUNT NOT FOUND")
        print("=" * 70)
        print()
        print("This could mean:")
        print("  1. You haven't created an account on Lighter yet")
        print("  2. The API endpoints have changed")
        print("  3. You're using testnet/mainnet mismatch")
        print()
        print("Next steps:")
        print("  • Visit https://lighter.xyz")
        print("  • Connect your wallet: " + l1_address)
        print("  • Complete account setup")
        print("  • Then run this script again")
        print()
    else:
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print(f"Your ACCOUNT_INDEX is: {account_index}")
        print()
        print("Update your .env file with:")
        print(f"  LIGHTER_ACCOUNT_INDEX={account_index}")
        print()

if __name__ == "__main__":
    main()
