#!/usr/bin/env python3
"""
Trading Strategies for Lighter Bot
Implements various trading strategies with risk management
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, client, config: Dict):
        self.client = client
        self.config = config
        self.positions = {}
        self.orders = {}
        
    async def analyze(self, market_data: Dict) -> Optional[str]:
        """
        Analyze market data and return signal
        Returns: 'buy', 'sell', or None
        """
        raise NotImplementedError
        
    async def execute_signal(self, signal: str, market_id: str, price: float):
        """Execute a trading signal"""
        raise NotImplementedError


class SimpleMarketMaker(TradingStrategy):
    """
    Simple Market Making Strategy
    Places buy and sell orders around the current price
    """
    
    def __init__(self, client, config: Dict):
        super().__init__(client, config)
        self.spread = config.get('spread', 0.001)  # 0.1% spread
        self.order_size = config.get('order_size', 0.01)  # Size per order
        self.max_position = config.get('max_position', 0.1)
        
    async def run(self, market_id: str):
        """Run the market making strategy"""
        logger.info(f"🎯 Starting Market Maker for {market_id}")
        logger.info(f"   Spread: {self.spread * 100}%")
        logger.info(f"   Order Size: {self.order_size}")
        
        while True:
            try:
                # Get current orderbook
                orderbook = await self.client.get_orderbook(market_id)
                
                if not orderbook:
                    logger.warning("⚠️  No orderbook data")
                    await asyncio.sleep(5)
                    continue
                
                # Calculate mid price
                best_bid = orderbook.get('best_bid', 0)
                best_ask = orderbook.get('best_ask', 0)
                
                if best_bid and best_ask:
                    mid_price = (best_bid + best_ask) / 2
                    
                    # Calculate our quote prices
                    our_bid = mid_price * (1 - self.spread / 2)
                    our_ask = mid_price * (1 + self.spread / 2)
                    
                    logger.info(f"📊 Market: {market_id}")
                    logger.info(f"   Mid Price: {mid_price:.4f}")
                    logger.info(f"   Our Bid: {our_bid:.4f}")
                    logger.info(f"   Our Ask: {our_ask:.4f}")
                    
                    # Place orders (implement based on SDK)
                    # await self.place_orders(market_id, our_bid, our_ask)
                    
                # Wait before next iteration
                await asyncio.sleep(self.config.get('interval', 10))
                
            except Exception as e:
                logger.error(f"❌ Error in market maker: {e}")
                await asyncio.sleep(5)


class MomentumStrategy(TradingStrategy):
    """
    Momentum Trading Strategy
    Buys when price is going up, sells when going down
    """
    
    def __init__(self, client, config: Dict):
        super().__init__(client, config)
        self.lookback_period = config.get('lookback_period', 20)
        self.threshold = config.get('threshold', 0.02)  # 2% move
        self.position_size = config.get('position_size', 0.1)
        self.price_history = {}
        
    async def run(self, market_id: str):
        """Run the momentum strategy"""
        logger.info(f"🎯 Starting Momentum Strategy for {market_id}")
        logger.info(f"   Lookback: {self.lookback_period} periods")
        logger.info(f"   Threshold: {self.threshold * 100}%")
        
        if market_id not in self.price_history:
            self.price_history[market_id] = []
        
        while True:
            try:
                # Get current price
                orderbook = await self.client.get_orderbook(market_id)
                
                if not orderbook:
                    await asyncio.sleep(5)
                    continue
                
                # Get mid price
                best_bid = orderbook.get('best_bid', 0)
                best_ask = orderbook.get('best_ask', 0)
                
                if not (best_bid and best_ask):
                    await asyncio.sleep(5)
                    continue
                    
                mid_price = (best_bid + best_ask) / 2
                
                # Add to history
                self.price_history[market_id].append({
                    'time': datetime.now(),
                    'price': mid_price
                })
                
                # Keep only recent history
                if len(self.price_history[market_id]) > self.lookback_period:
                    self.price_history[market_id].pop(0)
                
                # Calculate momentum
                if len(self.price_history[market_id]) >= self.lookback_period:
                    oldest_price = self.price_history[market_id][0]['price']
                    price_change = (mid_price - oldest_price) / oldest_price
                    
                    logger.info(f"📈 {market_id}: Price {mid_price:.4f}, Change: {price_change*100:.2f}%")
                    
                    # Generate signal
                    signal = None
                    if price_change > self.threshold:
                        signal = 'buy'
                        logger.info(f"🟢 BUY Signal! Momentum: {price_change*100:.2f}%")
                    elif price_change < -self.threshold:
                        signal = 'sell'
                        logger.info(f"🔴 SELL Signal! Momentum: {price_change*100:.2f}%")
                    
                    if signal:
                        await self.execute_signal(signal, market_id, mid_price)
                
                # Wait before next check
                await asyncio.sleep(self.config.get('interval', 60))
                
            except Exception as e:
                logger.error(f"❌ Error in momentum strategy: {e}")
                await asyncio.sleep(5)
    
    async def execute_signal(self, signal: str, market_id: str, price: float):
        """Execute a trading signal"""
        logger.info(f"📤 Executing {signal.upper()} for {market_id} at {price:.4f}")
        
        # Check if trading is enabled
        if not self.config.get('trading_enabled', False):
            logger.warning("⚠️  Trading is DISABLED (set trading_enabled=True to enable)")
            return
        
        # Implement order placement here based on Lighter SDK
        # Example:
        # if signal == 'buy':
        #     await self.client.create_order(...)
        # elif signal == 'sell':
        #     await self.client.create_order(...)


class GridTradingStrategy(TradingStrategy):
    """
    Grid Trading Strategy
    Places buy and sell orders at regular intervals
    """
    
    def __init__(self, client, config: Dict):
        super().__init__(client, config)
        self.grid_levels = config.get('grid_levels', 10)
        self.grid_spacing = config.get('grid_spacing', 0.01)  # 1%
        self.order_size = config.get('order_size', 0.01)
        
    async def run(self, market_id: str, base_price: float):
        """Run the grid trading strategy"""
        logger.info(f"🎯 Starting Grid Trading for {market_id}")
        logger.info(f"   Base Price: {base_price:.4f}")
        logger.info(f"   Grid Levels: {self.grid_levels}")
        logger.info(f"   Grid Spacing: {self.grid_spacing * 100}%")
        
        # Calculate grid levels
        grid_prices = []
        for i in range(-self.grid_levels // 2, self.grid_levels // 2 + 1):
            if i == 0:
                continue
            price = base_price * (1 + i * self.grid_spacing)
            side = 'buy' if i < 0 else 'sell'
            grid_prices.append({
                'level': i,
                'price': price,
                'side': side,
                'filled': False
            })
        
        logger.info(f"📊 Grid levels:")
        for level in grid_prices[:5]:
            logger.info(f"   {level['side'].upper()}: {level['price']:.4f}")
        logger.info(f"   ...")
        
        # Monitor and maintain grid
        while True:
            try:
                # Check filled orders and replace
                await self.maintain_grid(market_id, grid_prices)
                
                # Wait before next check
                await asyncio.sleep(self.config.get('interval', 30))
                
            except Exception as e:
                logger.error(f"❌ Error in grid strategy: {e}")
                await asyncio.sleep(5)
    
    async def maintain_grid(self, market_id: str, grid_prices: List[Dict]):
        """Maintain the grid by replacing filled orders"""
        # Get current orders
        # Check which orders are filled
        # Place new orders at grid levels
        pass


class ArbitrageStrategy(TradingStrategy):
    """
    Simple Arbitrage Strategy
    Looks for price differences between markets
    """
    
    def __init__(self, client, config: Dict):
        super().__init__(client, config)
        self.min_profit = config.get('min_profit', 0.005)  # 0.5% minimum profit
        self.markets = config.get('markets', [])
        
    async def run(self):
        """Run the arbitrage strategy"""
        logger.info(f"🎯 Starting Arbitrage Strategy")
        logger.info(f"   Min Profit: {self.min_profit * 100}%")
        logger.info(f"   Monitoring: {len(self.markets)} markets")
        
        while True:
            try:
                # Get prices from all markets
                prices = {}
                for market in self.markets:
                    orderbook = await self.client.get_orderbook(market)
                    if orderbook:
                        prices[market] = {
                            'bid': orderbook.get('best_bid', 0),
                            'ask': orderbook.get('best_ask', 0)
                        }
                
                # Find arbitrage opportunities
                await self.find_arbitrage(prices)
                
                # Wait before next scan
                await asyncio.sleep(self.config.get('interval', 5))
                
            except Exception as e:
                logger.error(f"❌ Error in arbitrage: {e}")
                await asyncio.sleep(5)
    
    async def find_arbitrage(self, prices: Dict):
        """Find and execute arbitrage opportunities"""
        for market1 in prices:
            for market2 in prices:
                if market1 == market2:
                    continue
                
                # Check if we can buy in market1 and sell in market2
                buy_price = prices[market1]['ask']
                sell_price = prices[market2]['bid']
                
                if buy_price and sell_price:
                    profit = (sell_price - buy_price) / buy_price
                    
                    if profit > self.min_profit:
                        logger.info(f"💰 ARBITRAGE OPPORTUNITY!")
                        logger.info(f"   Buy {market1} @ {buy_price:.4f}")
                        logger.info(f"   Sell {market2} @ {sell_price:.4f}")
                        logger.info(f"   Profit: {profit*100:.2f}%")
                        
                        if self.config.get('trading_enabled', False):
                            await self.execute_arbitrage(market1, market2, buy_price, sell_price)


class RiskManager:
    """
    Risk Management System
    Handles position sizing, stop losses, and risk limits
    """
    
    def __init__(self, config: Dict):
        self.max_position_size = config.get('max_position_size', 1.0)
        self.max_loss_per_trade = config.get('max_loss_per_trade', 0.02)  # 2%
        self.max_daily_loss = config.get('max_daily_loss', 0.05)  # 5%
        self.daily_pnl = 0
        self.positions = {}
        
    def calculate_position_size(self, account_balance: float, price: float) -> float:
        """Calculate safe position size"""
        # Risk-based position sizing
        risk_amount = account_balance * self.max_loss_per_trade
        position_size = min(
            risk_amount / price,
            self.max_position_size
        )
        return position_size
    
    def check_daily_loss_limit(self) -> bool:
        """Check if daily loss limit is exceeded"""
        return self.daily_pnl < -self.max_daily_loss
    
    def should_close_position(self, entry_price: float, current_price: float, side: str) -> bool:
        """Check if position should be closed (stop loss)"""
        if side == 'long':
            loss = (entry_price - current_price) / entry_price
        else:
            loss = (current_price - entry_price) / entry_price
        
        return loss > self.max_loss_per_trade
    
    def update_pnl(self, pnl: float):
        """Update daily P&L"""
        self.daily_pnl += pnl
        logger.info(f"📊 Daily P&L: {self.daily_pnl*100:.2f}%")


# Export strategies
STRATEGIES = {
    'market_maker': SimpleMarketMaker,
    'momentum': MomentumStrategy,
    'grid': GridTradingStrategy,
    'arbitrage': ArbitrageStrategy,
}
