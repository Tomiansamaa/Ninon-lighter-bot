#!/usr/bin/env python3
"""
Inspect the Lighter SDK to find available methods
"""

import lighter
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', 2))


async def inspect_client():
    print("🔍 Inspecting Lighter SDK...")
    print()
    
    # Initialize client
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    
    print("📦 SignerClient attributes and methods:")
    print("-" * 70)
    
    # Get all attributes
    attrs = [attr for attr in dir(client) if not attr.startswith('_')]
    
    for attr in attrs:
        attr_value = getattr(client, attr, None)
        attr_type = type(attr_value).__name__
        print(f"  • {attr:30s} : {attr_type}")
    
    print()
    print("📝 Looking for API methods...")
    
    # Check for common API patterns
    potential_apis = [
        'order_api', 'account_api', 'market_api', 'trade_api',
        'orders', 'accounts', 'markets', 'trades',
        'get_orderbook', 'get_account', 'get_balance',
        'orderbook', 'balance'
    ]
    
    print()
    print("🔍 Checking for common API patterns:")
    for api in potential_apis:
        if hasattr(client, api):
            print(f"  ✅ Found: {api}")
            obj = getattr(client, api)
            if callable(obj):
                print(f"     Type: method/function")
            else:
                print(f"     Type: {type(obj).__name__}")
                # If it's an object, check its methods
                if hasattr(obj, '__dict__'):
                    methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
                    if methods:
                        print(f"     Methods: {', '.join(methods[:10])}")
        else:
            print(f"  ❌ Not found: {api}")
    
    print()


if __name__ == "__main__":
    asyncio.run(inspect_client())

