#!/usr/bin/env python3
"""Test with both ETH private key and API private key"""

import asyncio
import os
from dotenv import load_dotenv
import lighter

load_dotenv()

async def test_keys():
    """Test both key types"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    eth_private_key = os.getenv('PRIVATE_KEY')
    api_key_private = os.getenv('LIGHTER_API_KEY_PRIVATE')
    account_index = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
    
    print("Testing Both Keys")
    print("=" * 70)
    print(f"\nETH Private Key: {eth_private_key[:10]}... (length: {len(eth_private_key)})")
    print(f"API Key Private: {api_key_private[:10]}... (length: {len(api_key_private)})")
    print(f"Account Index: {account_index}")
    
    # Test 1: With API Key Private (current setup)
    print("\n\n" + "=" * 70)
    print("TEST 1: Using API Key Private (current)")
    print("=" * 70)
    try:
        client1 = lighter.SignerClient(
            url=base_url,
            private_key=api_key_private,
            account_index=account_index,
            api_key_index=10
        )
        print("✅ Client initialized with API key private")
        
        # Try to place a small order
        import time
        order_result, tx_hash, order_id = await client1.create_market_order(
            market_index=1,
            client_order_index=int(time.time() * 1000) % 2147483647,
            base_amount=10000,  # Minimum
            avg_execution_price=115000,
            is_ask=False,
            reduce_only=False
        )
        print(f"✅ Order result: {tx_hash}")
        
    except Exception as e:
        print(f"❌ Failed with API key: {e}")
    
    # Test 2: With ETH Private Key
    print("\n\n" + "=" * 70)
    print("TEST 2: Using ETH Private Key")
    print("=" * 70)
    try:
        client2 = lighter.SignerClient(
            url=base_url,
            private_key=eth_private_key,
            account_index=account_index,
            api_key_index=10
        )
        print("✅ Client initialized with ETH private key")
        
        # Try to place a small order
        import time
        order_result, tx_hash, order_id = await client2.create_market_order(
            market_index=1,
            client_order_index=int(time.time() * 1000) % 2147483647,
            base_amount=10000,  # Minimum
            avg_execution_price=115000,
            is_ask=False,
            reduce_only=False
        )
        print(f"✅ Order result: {tx_hash}")
        
    except Exception as e:
        print(f"❌ Failed with ETH key: {e}")
    
    # Test 3: With ETH Private Key and api_key_index=0
    print("\n\n" + "=" * 70)
    print("TEST 3: Using ETH Private Key + api_key_index=0")
    print("=" * 70)
    try:
        client3 = lighter.SignerClient(
            url=base_url,
            private_key=eth_private_key,
            account_index=account_index,
            api_key_index=0
        )
        print("✅ Client initialized with ETH key + index 0")
        
        # Try to place a small order
        import time
        order_result, tx_hash, order_id = await client3.create_market_order(
            market_index=1,
            client_order_index=int(time.time() * 1000) % 2147483647,
            base_amount=10000,  # Minimum
            avg_execution_price=115000,
            is_ask=False,
            reduce_only=False
        )
        print(f"✅ Order result: {tx_hash}")
        
    except Exception as e:
        print(f"❌ Failed with ETH key + index 0: {e}")

if __name__ == "__main__":
    asyncio.run(test_keys())

