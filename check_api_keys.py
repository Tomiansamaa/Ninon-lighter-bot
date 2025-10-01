#!/usr/bin/env python3
"""Check API keys for the account"""

import asyncio
import os
from dotenv import load_dotenv
import lighter

load_dotenv()

async def check_api_keys():
    """Check what API keys exist for this account"""
    
    # Configuration
    base_url = os.getenv('LIGHTER_API_URL')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print(f"Account Index: {account_index}")
    print(f"Checking API keys...\n")
    
    try:
        # Initialize client
        client = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=2  # Current setting
        )
        
        # Try to get account API keys info
        # Use ApiClient to query account API keys
        api_client = lighter.ApiClient(base_url)
        account_api = lighter.AccountApi(api_client)
        
        # Get API keys for this account (255 = all keys)
        result = await account_api.apikeys(account_index, 255)
        
        print("API Keys for this account:")
        print("=" * 70)
        
        if hasattr(result, 'apikeys'):
            for key in result.apikeys:
                print(f"Index: {key.index}")
                print(f"  Public Key: {key.apikey[:32]}...")
                print(f"  Status: Active" if key.index else "Status: Unknown")
                print()
        else:
            print("No API keys found or unable to parse response")
            print(f"Response: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_api_keys())

