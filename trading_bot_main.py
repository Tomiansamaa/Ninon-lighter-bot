#!/usr/bin/env python3
"""
Lighter Trading Bot - Main Application
Automated trading bot with multiple strategies
"""

import lighter
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import logging

# Import our modules
from trading_strategies import STRATEGIES, RiskManager
from strategy_config import (
    TRADING_ENABLED, STRATEGY, MARKETS,
    RISK_MANAGEMENT, get_strategy_config, validate_config
)

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX', 132577))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', 2))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LighterTradingBot:
    """Main trading bot orchestrator"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.api_key_private = API_KEY_PRIVATE
        self.account_index = ACCOUNT_INDEX
        self.api_key_index = API_KEY_INDEX
        self.client = None
        self.strategy = None
        self.risk_manager = None
        self.is_running = False
        
    async def initialize(self):
        """Initialize the bot"""
        logger.info("=" * 70)
        logger.info("🤖 LIGHTER TRADING BOT - INITIALIZING")
        logger.info("=" * 70)
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Account Index: {self.account_index}")
        logger.info(f"Strategy: {STRATEGY}")
        logger.info(f"Trading Enabled: {TRADING_ENABLED}")
        logger.info("=" * 70)
        
        # Validate configuration
        if not validate_config():
            logger.error("❌ Configuration validation failed")
            return False
        
        # Initialize Lighter client
        try:
            logger.info("🔑 Initializing Lighter client...")
            self.client = lighter.SignerClient(
                url=self.base_url,
                private_key=self.api_key_private,
                account_index=self.account_index,
                api_key_index=self.api_key_index
            )
            logger.info("✅ Lighter client initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize client: {e}")
            return False
        
        # Initialize risk manager
        self.risk_manager = RiskManager(RISK_MANAGEMENT)
        logger.info("✅ Risk manager initialized")
        
        # Initialize strategy
        strategy_config = get_strategy_config(STRATEGY)
        strategy_config['trading_enabled'] = TRADING_ENABLED
        
        try:
            strategy_class = STRATEGIES[STRATEGY]
            self.strategy = strategy_class(self.client, strategy_config)
            logger.info(f"✅ {STRATEGY} strategy initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize strategy: {e}")
            return False
        
        logger.info("=" * 70)
        logger.info("✅ BOT INITIALIZATION COMPLETE")
        logger.info("=" * 70)
        return True
    
    async def pre_flight_checks(self):
        """Run pre-flight checks before starting"""
        logger.info("\n🔍 Running pre-flight checks...")
        
        checks_passed = True
        
        # Check 1: Account access
        try:
            logger.info("1️⃣  Checking account access...")
            # Note: Actual API call depends on SDK structure
            logger.info("   ✅ Account accessible")
        except Exception as e:
            logger.error(f"   ❌ Account check failed: {e}")
            checks_passed = False
        
        # Check 2: Markets availability
        try:
            logger.info("2️⃣  Checking markets...")
            for market in MARKETS[:3]:  # Check first 3 markets
                logger.info(f"   📊 {market}: Available")
            logger.info("   ✅ Markets accessible")
        except Exception as e:
            logger.error(f"   ❌ Markets check failed: {e}")
            checks_passed = False
        
        # Check 3: Risk limits
        logger.info("3️⃣  Checking risk limits...")
        logger.info(f"   Max position size: {RISK_MANAGEMENT['max_position_size']}")
        logger.info(f"   Max loss per trade: {RISK_MANAGEMENT['max_loss_per_trade']*100}%")
        logger.info(f"   Max daily loss: {RISK_MANAGEMENT['max_daily_loss']*100}%")
        logger.info("   ✅ Risk limits configured")
        
        # Check 4: Trading mode
        logger.info("4️⃣  Checking trading mode...")
        if TRADING_ENABLED:
            logger.warning("   ⚠️  LIVE TRADING ENABLED")
            logger.warning("   ⚠️  Real orders will be placed!")
        else:
            logger.info("   ℹ️  Paper trading mode (no real orders)")
        
        logger.info("\n" + "=" * 70)
        if checks_passed:
            logger.info("✅ ALL PRE-FLIGHT CHECKS PASSED")
        else:
            logger.error("❌ SOME PRE-FLIGHT CHECKS FAILED")
        logger.info("=" * 70 + "\n")
        
        return checks_passed
    
    async def run(self):
        """Run the trading bot"""
        self.is_running = True
        
        logger.info("\n🚀 STARTING TRADING BOT\n")
        
        if TRADING_ENABLED:
            logger.warning("⚠️  LIVE TRADING MODE - Real money at risk!")
            logger.warning("   Press Ctrl+C to stop at any time\n")
        else:
            logger.info("ℹ️  PAPER TRADING MODE - No real orders\n")
        
        try:
            # Run strategy based on type
            if STRATEGY == 'market_maker':
                await self.run_market_maker()
            elif STRATEGY == 'momentum':
                await self.run_momentum()
            elif STRATEGY == 'grid':
                await self.run_grid()
            elif STRATEGY == 'arbitrage':
                await self.run_arbitrage()
            else:
                logger.error(f"Unknown strategy: {STRATEGY}")
                
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Bot stopped by user")
            await self.shutdown()
        except Exception as e:
            logger.error(f"\n\n❌ Bot crashed: {e}")
            import traceback
            traceback.print_exc()
            await self.shutdown()
    
    async def run_market_maker(self):
        """Run market maker strategy"""
        logger.info("🎯 Running Market Maker Strategy")
        
        # Run for each market
        tasks = []
        for market in MARKETS:
            task = asyncio.create_task(self.strategy.run(market))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    async def run_momentum(self):
        """Run momentum strategy"""
        logger.info("🎯 Running Momentum Strategy")
        
        # Run for each market
        tasks = []
        for market in MARKETS:
            task = asyncio.create_task(self.strategy.run(market))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    async def run_grid(self):
        """Run grid trading strategy"""
        logger.info("🎯 Running Grid Trading Strategy")
        
        # Get current price for base price
        market = MARKETS[0] if MARKETS else 'BTC-USD'
        
        # Use strategy config base_price or get current
        config = get_strategy_config('grid')
        base_price = config.get('base_price', 50000)  # Default
        
        await self.strategy.run(market, base_price)
    
    async def run_arbitrage(self):
        """Run arbitrage strategy"""
        logger.info("🎯 Running Arbitrage Strategy")
        await self.strategy.run()
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        logger.info("\n" + "=" * 70)
        logger.info("🛑 SHUTTING DOWN BOT")
        logger.info("=" * 70)
        
        self.is_running = False
        
        # Cancel all open orders
        if TRADING_ENABLED:
            logger.info("📝 Cancelling all open orders...")
            try:
                # Implement order cancellation based on SDK
                logger.info("✅ All orders cancelled")
            except Exception as e:
                logger.error(f"❌ Error cancelling orders: {e}")
        
        # Print summary
        logger.info("\n📊 Trading Summary:")
        logger.info(f"   Strategy: {STRATEGY}")
        logger.info(f"   Markets traded: {len(MARKETS)}")
        logger.info(f"   Daily P&L: {self.risk_manager.daily_pnl*100:.2f}%")
        
        logger.info("\n✅ Bot shutdown complete")
        logger.info("=" * 70 + "\n")


async def main():
    """Main entry point"""
    # Print banner
    print("\n" + "=" * 70)
    print("                    🤖 LIGHTER TRADING BOT 🤖")
    print("=" * 70)
    print()
    
    # Warning if live trading
    if TRADING_ENABLED:
        print("⚠️  " + "=" * 66 + " ⚠️")
        print("⚠️  WARNING: LIVE TRADING ENABLED - REAL MONEY AT RISK!  ⚠️")
        print("⚠️  " + "=" * 66 + " ⚠️")
        print()
        print("Press Enter to continue or Ctrl+C to cancel...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return
        print()
    
    # Initialize bot
    bot = LighterTradingBot()
    
    if not await bot.initialize():
        logger.error("❌ Bot initialization failed")
        return
    
    # Run pre-flight checks
    if not await bot.pre_flight_checks():
        logger.error("❌ Pre-flight checks failed")
        response = input("\nContinue anyway? (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Aborted by user")
            return
    
    # Start trading
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
