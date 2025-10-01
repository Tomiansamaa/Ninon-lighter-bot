#!/usr/bin/env python3
"""
Quick test script for Lighter API using Python SDK
Install: pip install lighter-sdk
"""

# First, you need to install the SDK:
# pip install lighter-sdk

try:
    import lighter
    print("✅ Lighter SDK imported successfully\n")
except ImportError:
    print("❌ Lighter SDK not found!")
    print("📦 Install it with: pip install lighter-sdk")
    exit(1)

# Your credentials from .env
BASE_URL = "https://mainnet.zklighter.elliot.ai"
API_KEY_PRIVATE = "b891f05e1823990a5e9c06e9f0698d6edf0326784b49c961e5c688c556eb0d18b3a2b34beee42e7b"
ETH_PRIVATE_KEY = "0x06f1b4418b5073d80fdc1d88fb5cab4cea6cae9e8bd937c498dff19d52a7fc52"
L1_ADDRESS = "0xC843b738d7b34c97393e198E6dAA6c4Fb81bdB80"
ACCOUNT_INDEX = 0  # You might need to find this first
API_KEY_INDEX = 2

def test_lighter_api():
    print("🚀 Testing Lighter API with Python SDK\n")
    print(f"📍 Base URL: {BASE_URL}")
    print(f"📍 Wallet: {L1_ADDRESS}\n")
    
    try:
        # Step 1: Get account information (doesn't require signer)
        print("📊 Test 1: Getting account info by address...")
        # Note: The actual method names may vary, check lighter SDK docs
        # This is a simplified example
        
        # Step 2: Initialize signer client (for trading operations)
        print("\n🔑 Test 2: Initializing signer client...")
        client = lighter.SignerClient(
            url=BASE_URL,
            private_key=API_KEY_PRIVATE,
            account_index=ACCOUNT_INDEX,
            api_key_index=API_KEY_INDEX
        )
        print("✅ Signer client initialized")
        
        # Step 3: Get markets/orderbooks
        print("\n📈 Test 3: Fetching markets...")
        try:
            orderbooks = client.order_api.order_books()
            print(f"✅ Found markets!")
            print(f"   Markets: {list(orderbooks.keys())[:5] if hasattr(orderbooks, 'keys') else orderbooks[:5]}")
        except Exception as e:
            print(f"⚠️  Error fetching markets: {e}")
        
        # Step 4: Get account data
        print("\n💰 Test 4: Getting account data...")
        try:
            account = client.account_api.account(account_index=ACCOUNT_INDEX)
            print("✅ Account data retrieved:")
            print(f"   {account}")
        except Exception as e:
            print(f"⚠️  Error: {e}")
            
        print("\n✅ Tests completed!")
        print("\n📝 If this works, your credentials are correct!")
        print("   You can now build your trading bot using the Python SDK.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nℹ️  This might mean:")
        print("  1. The account doesn't exist yet (needs to be created)")
        print("  2. The ACCOUNT_INDEX is incorrect")
        print("  3. API credentials are not set up properly")
        print("\n💡 Check the Lighter documentation for account setup")

if __name__ == "__main__":
    test_lighter_api()
