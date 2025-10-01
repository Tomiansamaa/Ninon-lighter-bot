#!/usr/bin/env python3
"""Setup API key for trading"""

import asyncio
import os
from dotenv import load_dotenv
import lighter

load_dotenv()

async def setup_api_key():
    """Create/register an API key for the account"""
    
    # Configuration
    base_url = os.getenv('LIGHTER_API_URL')
    eth_private_key = os.getenv('PRIVATE_KEY')  # L1 ETH private key
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    api_key_index = int(os.getenv('LIGHTER_API_KEY_INDEX', '2'))
    
    print(f"Account Index: {account_index}")
    print(f"API Key Index: {api_key_index}")
    print(f"Setting up API key...\n")
    
    try:
        # Initialize client with ETH private key (not API key)
        # For creating API key, we use the L1 wallet
        client = lighter.SignerClient(
            url=base_url,
            private_key=eth_private_key,
            account_index=account_index,
            api_key_index=0  # Use index 0 (desktop) temporarily to create the key
        )
        
        # The API key public/private from .env
        api_key_public = os.getenv('LIGHTER_API_KEY_PUBLIC')
        api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
        
        print(f"API Key Public: {api_key_public[:32]}...")
        print(f"API Key Index to register: {api_key_index}")
        print()
        
        # Create/register the API key
        print("Creating API key transaction...")
        result = await client.create_api_key(
            api_key=api_key_public,
            api_key_index=api_key_index
        )
        
        print(f"✅ API Key registered!")
        print(f"Transaction: {result}")
        print()
        print("You can now use this API key for trading.")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("POSSIBLE SOLUTIONS:")
        print("=" * 70)
        print("1. The API key might already be registered")
        print("2. You might need to use index 0 or 1 instead of 2")
        print("3. The API key might be for a different account")
        print()
        print("Try changing LIGHTER_API_KEY_INDEX in .env to:")
        print("  - 0 (for desktop)")
        print("  - 1 (for mobile)")

if __name__ == "__main__":
    asyncio.run(setup_api_key())

