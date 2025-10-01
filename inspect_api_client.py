#!/usr/bin/env python3
"""
Inspect the api_client to find data fetching methods
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


async def inspect_api_client():
    print("🔍 Inspecting ApiClient...")
    print()
    
    # Initialize client
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    
    api_client = client.api_client
    
    print("📦 ApiClient attributes and methods:")
    print("-" * 70)
    
    # Get all attributes
    attrs = [attr for attr in dir(api_client) if not attr.startswith('_')]
    
    for attr in attrs:
        attr_value = getattr(api_client, attr, None)
        attr_type = type(attr_value).__name__
        print(f"  • {attr:30s} : {attr_type}")
        
        # If it's not a simple type, check its methods
        if attr_type not in ['str', 'int', 'float', 'bool', 'dict', 'list', 'NoneType', 'function', 'method']:
            methods = [m for m in dir(attr_value) if not m.startswith('_') and callable(getattr(attr_value, m, None))]
            if methods:
                print(f"     └─ Methods: {', '.join(methods[:10])}")
    
    print()


if __name__ == "__main__":
    asyncio.run(inspect_api_client())

