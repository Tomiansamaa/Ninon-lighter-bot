#!/usr/bin/env python3
"""
Lighter Aggressive Leverage Bot
Implements the high-risk 50x leverage strategy with trailing stops
"""

import lighter
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import logging

# Import strategy
from aggressive_leverage_strategy import AggressiveLeverageStrategy
from aggressive_bot_config import (
    TRADING_ENABLED, MARKET, MARKET_ID,
    AGGRESSIVE_STRATEGY_CONFIG,
    validate_config, display_risks
)
# Import API wrapper for real price data
from lighter_api_wrapper import LighterAPIWrapper

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', 10))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aggressive_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AggressiveTradingBot:
    """Main bot for aggressive leverage trading"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key_private = API_KEY_PRIVATE
        self.account_index = ACCOUNT_INDEX
        self.api_key_index = API_KEY_INDEX
        self.client = None
        self.api_wrapper = None
        self.strategy = None
        self.is_running = False
        self.daily_stats = {
            'start_balance': 0,
            'trades': 0,
            'wins': 0,
            'losses': 0,
            'total_pnl': 0
        }
        
    async def initialize(self):
        """Initialize the bot"""
        print("\n" + "=" * 70)
        print("⚡ AGGRESSIVE LEVERAGE TRADING BOT")
        print("=" * 70)
        print()
        
        # Validate configuration
        if not validate_config():
            return False
        
        # Initialize Lighter client
        try:
            logger.info("🔑 Initializing Lighter client...")
            logger.info(f"   Using API key index {self.api_key_index}")
            self.client = lighter.SignerClient(
                url=self.base_url,
                private_key=self.api_key_private,
                account_index=self.account_index,
                api_key_index=self.api_key_index
            )
            logger.info("✅ Lighter client initialized")
            
            # Initialize API wrapper for real-time data
            logger.info("📡 Initializing API wrapper for real-time prices...")
            self.api_wrapper = LighterAPIWrapper(self.base_url)
            logger.info("✅ API wrapper initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize client: {e}")
            return False
        
        # Initialize strategy
        try:
            # Pass both signer client and API wrapper to strategy
            strategy_config = AGGRESSIVE_STRATEGY_CONFIG.copy()
            strategy_config['api_wrapper'] = self.api_wrapper
            strategy_config['account_index'] = self.account_index
            
            self.strategy = AggressiveLeverageStrategy(
                self.client,
                strategy_config
            )
            logger.info("✅ Aggressive strategy initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize strategy: {e}")
            return False
        
        print()
        logger.info("=" * 70)
        logger.info("✅ BOT INITIALIZATION COMPLETE")
        logger.info("=" * 70)
        print()
        
        return True
    
    async def display_strategy_info(self):
        """Display strategy information"""
        print("📋 STRATEGY DETAILS:")
        print("=" * 70)
        print(f"🎯 Market: {MARKET}")
        print(f"💰 Position Size: {AGGRESSIVE_STRATEGY_CONFIG['position_size_percent']*100}% of balance")
        print(f"⚡ Leverage: {AGGRESSIVE_STRATEGY_CONFIG['leverage']}x")
        print(f"📈 Profit Thresholds: {AGGRESSIVE_STRATEGY_CONFIG['profit_thresholds']}")
        print(f"📉 Double Down at: {AGGRESSIVE_STRATEGY_CONFIG['double_down_threshold']}%")
        print(f"⏱️  Cooldown: {AGGRESSIVE_STRATEGY_CONFIG['cooldown_seconds']}s")
        print(f"🔄 Check Interval: {AGGRESSIVE_STRATEGY_CONFIG['check_interval']}s")
        print()
        print("TRAILING STOP LOGIC:")
        print("-" * 70)
        for threshold in AGGRESSIVE_STRATEGY_CONFIG['profit_thresholds'][:5]:
            stop = threshold - 1
            print(f"  • At +{threshold}% profit → Stop Loss at +{stop}%")
        print("  • ... and so on")
        print()
        print("MARTINGALE (DOUBLING):")
        print("-" * 70)
        print(f"  • If position reaches {AGGRESSIVE_STRATEGY_CONFIG['double_down_threshold']}%")
        print(f"  • Double the position size to average down")
        print(f"  • ⚠️  Can lead to very large losses!")
        print()
        print("=" * 70)
        print()
    
    async def run(self):
        """Run the trading bot"""
        self.is_running = True
        
        await self.display_strategy_info()
        
        if TRADING_ENABLED:
            print("⚠️  LIVE TRADING MODE - REAL MONEY AT RISK!")
            print()
        else:
            print("ℹ️  PAPER TRADING MODE (Safe - No Real Orders)")
            print()
        
        logger.info("🚀 Starting aggressive leverage strategy...")
        logger.info(f"   Market: {MARKET}")
        logger.info(f"   Mode: {'LIVE TRADING' if TRADING_ENABLED else 'PAPER TRADING'}")
        print()
        
        try:
            # Run the strategy
            await self.strategy.run(MARKET_ID)
            
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Bot stopped by user")
            await self.shutdown()
        except Exception as e:
            logger.error(f"\n\n❌ Bot crashed: {e}")
            import traceback
            traceback.print_exc()
            await self.shutdown()
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        logger.info("\n" + "=" * 70)
        logger.info("🛑 SHUTTING DOWN BOT")
        logger.info("=" * 70)
        
        self.is_running = False
        
        # Close API wrapper
        if self.api_wrapper:
            await self.api_wrapper.close()
        
        # Get final stats
        if self.strategy:
            stats = self.strategy.get_stats()
            logger.info("\n📊 Final Status:")
            logger.info(f"   Position Active: {stats['position_active']}")
            if stats['position_active']:
                logger.info(f"   Entry Price: ${stats['entry_price']:.2f}")
                logger.info(f"   Side: {stats['current_side']}")
                logger.info(f"   Has Doubled: {stats['has_doubled']}")
                logger.info(f"   Highest Profit: {stats['highest_profit']:.2f}%")
                logger.info(f"   Current Stop Loss: {stats['current_stop_loss']}")
        
        logger.info("\n✅ Bot shutdown complete")
        logger.info("=" * 70 + "\n")


async def main():
    """Main entry point"""
    # Initialize and run bot
    bot = AggressiveTradingBot()
    
    if not await bot.initialize():
        logger.error("❌ Bot initialization failed")
        return
    
    # Run the bot
    await bot.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
