#!/usr/bin/env python3
"""
Lighter Trading Bot - Python Implementation
Uses official Lighter SDK with async support
"""

import lighter
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 0))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', 2))

class LighterBot:
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key_private = API_KEY_PRIVATE
        self.account_index = ACCOUNT_INDEX
        self.api_key_index = API_KEY_INDEX
        self.client = None
        
        print("🤖 Initializing Lighter Trading Bot...")
        print(f"   Base URL: {self.base_url}")
        print(f"   Account Index: {self.account_index}")
        print(f"   API Key Index: {self.api_key_index}\n")
    
    async def initialize(self):
        """Initialize the Lighter client"""
        try:
            print("🔑 Initializing Lighter SignerClient...")
            
            # Initialize within async context
            self.client = lighter.SignerClient(
                url=self.base_url,
                private_key=self.api_key_private,
                account_index=self.account_index,
                api_key_index=self.api_key_index
            )
            
            print("✅ Client initialized successfully\n")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize client: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def get_account_info(self):
        """Get account information"""
        try:
            print("📊 Fetching account information...")
            account = await self.client.account_api.account(account_index=self.account_index)
            print("✅ Account data:")
            print(f"   {account}\n")
            return account
        except Exception as e:
            print(f"⚠️  Could not fetch account: {e}\n")
            return None
    
    async def get_markets(self):
        """Get all available markets"""
        try:
            print("📈 Fetching available markets...")
            orderbooks = await self.client.order_api.order_books()
            
            if isinstance(orderbooks, dict):
                markets = list(orderbooks.keys())
                print(f"✅ Found {len(markets)} markets")
                if len(markets) > 0:
                    print(f"\nFirst 10 markets:")
                    for i, market in enumerate(markets[:10], 1):
                        print(f"   {i}. {market}")
                print()
                return orderbooks
            else:
                print(f"✅ Markets: {orderbooks}\n")
                return orderbooks
        except Exception as e:
            print(f"⚠️  Could not fetch markets: {e}\n")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_orderbook(self, market_id):
        """Get orderbook for a specific market"""
        try:
            print(f"📖 Fetching orderbook for {market_id}...")
            orderbook = await self.client.order_api.order_book_details(market_id)
            print(f"✅ Orderbook for {market_id}:")
            print(f"   Bids: {len(orderbook.get('bids', []))} orders")
            print(f"   Asks: {len(orderbook.get('asks', []))} orders\n")
            return orderbook
        except Exception as e:
            print(f"⚠️  Could not fetch orderbook: {e}\n")
            return None
    
    async def get_orders(self):
        """Get active orders"""
        try:
            print("📝 Fetching active orders...")
            orders = await self.client.order_api.orders(self.account_index)
            print(f"✅ Active orders: {len(orders) if isinstance(orders, list) else 'N/A'}")
            if orders:
                print(f"   {orders[:5]}")  # Show first 5
            print()
            return orders
        except Exception as e:
            print(f"⚠️  Could not fetch orders: {e}\n")
            return None
    
    async def get_trades(self):
        """Get trade history"""
        try:
            print("💱 Fetching trade history...")
            trades = await self.client.order_api.trades(self.account_index)
            print(f"✅ Recent trades: {len(trades) if isinstance(trades, list) else 'N/A'}")
            if trades:
                print(f"   {trades[:5]}")  # Show first 5
            print()
            return trades
        except Exception as e:
            print(f"⚠️  Could not fetch trades: {e}\n")
            return None
    
    async def run_tests(self):
        """Run all connection tests"""
        print("🧪 Running connection tests...\n")
        
        # Test 1: Get account info
        await self.get_account_info()
        
        # Test 2: Get markets
        markets = await self.get_markets()
        
        # Test 3: Get orders
        await self.get_orders()
        
        # Test 4: Get trades
        await self.get_trades()
        
        print("✅ All tests completed!\n")
        return markets

async def main():
    """Main async entry point"""
    print("=" * 70)
    print("🚀 LIGHTER TRADING BOT - PYTHON")
    print("=" * 70)
    print()
    
    # Initialize bot
    bot = LighterBot()
    
    if not await bot.initialize():
        print("❌ Failed to initialize bot. Check your credentials.")
        return
    
    # Run tests
    markets = await bot.run_tests()
    
    print("=" * 70)
    print("📊 CONNECTION SUCCESSFUL!")
    print("=" * 70)
    print()
    print("Your Lighter API credentials are working!")
    print()
    print("Next steps:")
    print("  • Review the bot code in lighter_bot.py")
    print("  • Customize trading strategies")
    print("  • Check Lighter docs: https://apidocs.lighter.xyz/docs")
    print()
    print("Available methods:")
    print("  • get_markets() - Get all trading pairs")
    print("  • get_orderbook(market_id) - Get market depth")
    print("  • get_orders() - Get your active orders")
    print("  • get_trades() - Get your trade history")
    print()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())