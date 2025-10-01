#!/usr/bin/env python3
"""Find which account the API key belongs to"""

import asyncio
import os
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper

load_dotenv()

async def find_api_key_account():
    """Find the account associated with the API keys"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    l1_address = "0xC843b738d7b34c97393e198E6dAA6c4Fb81bdB80"  # Your wallet
    
    print(f"Checking accounts for wallet: {l1_address}")
    print("=" * 70)
    
    async with LighterAPIWrapper(base_url) as api:
        # Get all accounts for this L1 address
        url = f"{base_url}/api/v1/account?by=l1_address&value={l1_address}"
        
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'accounts' in data:
                        print(f"Found {len(data['accounts'])} account(s):\n")
                        
                        for acc in data['accounts']:
                            index = acc.get('account_index')
                            balance = float(acc.get('available_balance', 0))
                            
                            print(f"Account Index: {index}")
                            print(f"Balance: ${balance:.2f}")
                            print(f"Is Master: {acc.get('is_master_account', False)}")
                            print()
                            
                            # Try to get API keys for this account
                            keys_url = f"{base_url}/api/v1/account/apikeys?account_index={index}&api_key_index=255"
                            async with session.get(keys_url) as keys_resp:
                                if keys_resp.status == 200:
                                    keys_data = await keys_resp.json()
                                    if 'apikeys' in keys_data and keys_data['apikeys']:
                                        print(f"  API Keys:")
                                        for key in keys_data['apikeys']:
                                            key_index = key.get('index', 'Unknown')
                                            key_pub = key.get('apikey', 'Unknown')[:32]
                                            print(f"    Index {key_index}: {key_pub}...")
                                        print()
                                    else:
                                        print(f"  No API keys found")
                                        print()
                                else:
                                    print(f"  Couldn't fetch API keys")
                                    print()
                            
                            print("-" * 70)
                        
                        print("\n💡 RECOMMENDATION:")
                        print("=" * 70)
                        print("The API keys in your .env might not be registered to any account.")
                        print("You should use your ETH private key directly instead.")
                        print()
                        print("Your ETH private key (PRIVATE_KEY in .env) can sign transactions")
                        print("directly without needing separate API keys.")
                    else:
                        print("No accounts found")
                else:
                    print(f"Error: HTTP {response.status}")
                    print(await response.text())

if __name__ == "__main__":
    asyncio.run(find_api_key_account())

