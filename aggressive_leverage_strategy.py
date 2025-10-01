#!/usr/bin/env python3
"""
Aggressive Leverage Strategy for Lighter
High-risk, high-reward strategy with trailing stops and position doubling

Strategy:
1. Open position with 5% of balance at 50x leverage
2. Trailing stop loss:
   - At +2% profit → stop loss at -1%
   - At +3% profit → stop loss at -2%
   - At +4% profit → stop loss at -3%
   - Continue pattern...
3. If position hits -6%:
   - Double the position size at current price (average down)
4. When stop loss triggers:
   - Wait a bit (cooldown)
   - Open new position

⚠️  WARNING: EXTREMELY HIGH RISK!
   - 50x leverage means 2% move = 100% position loss
   - Martingale (doubling) can lead to massive losses
   - Only use with money you can afford to lose completely
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AggressiveLeverageStrategy:
    """
    Aggressive 50x leverage strategy with trailing stops and position doubling
    """
    
    def __init__(self, client, config: Dict):
        self.client = client
        self.config = config
        
        # API wrapper for real-time data
        self.api_wrapper = config.get('api_wrapper')
        self.account_index = config.get('account_index')
        
        # Strategy parameters
        self.position_size_percent = config.get('position_size_percent', 0.05)  # 5%
        self.leverage = config.get('leverage', 50)  # 50x
        self.profit_thresholds = config.get('profit_thresholds', [2, 3, 4, 5, 6, 7, 8, 9, 10])  # %
        self.stop_loss_offset = 1  # Stop loss is always 1% below profit threshold
        self.double_down_threshold = config.get('double_down_threshold', -6)  # -6%
        self.cooldown_seconds = config.get('cooldown_seconds', 60)  # Wait after stop loss
        self.check_interval = config.get('check_interval', 5)  # Check every 5 seconds
        
        # Position tracking
        self.current_position = None
        self.entry_price = None
        self.position_size = None
        self.current_side = None
        self.has_doubled = False
        self.highest_profit = 0
        self.current_stop_loss = None
        self.last_stop_loss_time = None
        
        logger.info("🎯 Aggressive Leverage Strategy Initialized")
        logger.info(f"   Position Size: {self.position_size_percent*100}% of balance")
        logger.info(f"   Leverage: {self.leverage}x")
        logger.info(f"   Double Down at: {self.double_down_threshold}%")
        logger.info(f"   Cooldown: {self.cooldown_seconds}s")
        
    async def run(self, market_id: str):
        """Run the aggressive leverage strategy"""
        logger.info("=" * 70)
        logger.info(f"🚀 STARTING AGGRESSIVE LEVERAGE STRATEGY")
        logger.info(f"   Market: {market_id}")
        logger.info(f"   Leverage: {self.leverage}x")
        logger.info("=" * 70)
        logger.warning("⚠️  EXTREMELY HIGH RISK STRATEGY!")
        logger.warning("⚠️  50x LEVERAGE CAN LIQUIDATE QUICKLY!")
        logger.warning("⚠️  USE ONLY WITH MONEY YOU CAN AFFORD TO LOSE!")
        logger.info("=" * 70)
        
        while True:
            try:
                # Check if we're in cooldown
                if self.is_in_cooldown():
                    logger.info(f"⏸️  Cooldown period active...")
                    await asyncio.sleep(self.check_interval)
                    continue
                
                # If no position, open one
                if not self.current_position:
                    await self.open_new_position(market_id)
                else:
                    # Monitor existing position
                    await self.monitor_position(market_id)
                
                # Wait before next check
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in strategy loop: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(self.check_interval)
    
    def is_in_cooldown(self) -> bool:
        """Check if we're in cooldown period after stop loss"""
        if not self.last_stop_loss_time:
            return False
        
        cooldown_end = self.last_stop_loss_time + timedelta(seconds=self.cooldown_seconds)
        if datetime.now() < cooldown_end:
            remaining = (cooldown_end - datetime.now()).seconds
            if remaining % 10 == 0:  # Log every 10 seconds
                logger.info(f"   Cooldown: {remaining}s remaining...")
            return True
        
        return False
    
    async def get_account_balance(self) -> float:
        """Get available account balance from Lighter API"""
        try:
            if not self.api_wrapper or not self.account_index:
                logger.warning("⚠️  API wrapper not configured, using fallback")
                return 100.0
            
            # Get account data from API wrapper
            account_data = await self.api_wrapper.get_account(self.account_index)
            
            if not account_data or 'accounts' not in account_data:
                logger.error("❌ No account data received")
                return 100.0
            
            accounts = account_data['accounts']
            if not accounts:
                logger.error("❌ No accounts found")
                return 100.0
            
            acc = accounts[0]
            balance = float(acc.get('available_balance', 0))
            
            logger.debug(f"💰 Real Account Balance: ${balance:.2f}")
            return balance
            
        except Exception as e:
            logger.error(f"❌ Failed to get balance: {e}")
            import traceback
            traceback.print_exc()
            return 100.0
    
    async def get_current_price(self, market_id: int) -> Optional[float]:
        """Get current market price from Lighter API"""
        try:
            if not self.api_wrapper:
                logger.error("❌ API wrapper not configured")
                return None
            
            # Get orderbook from API
            orderbook_data = await self.api_wrapper.get_orderbook(market_id)
            
            if not orderbook_data or 'order_book_details' not in orderbook_data:
                logger.error("❌ No orderbook data received")
                return None
            
            # Find the market in the details
            order_books = orderbook_data['order_book_details']
            if not order_books:
                logger.error("❌ Orderbook details empty")
                return None
            
            # Get the first orderbook (should be the one we requested)
            ob = order_books[0]
            
            # Check if there's last_trade_price or mark_price
            if 'last_trade_price' in ob:
                price = float(ob['last_trade_price'])
                logger.debug(f"📊 {ob.get('symbol', 'Unknown')} Price: ${price:,.2f}")
                return price
            elif 'mark_price' in ob:
                price = float(ob['mark_price'])
                logger.debug(f"📊 {ob.get('symbol', 'Unknown')} Mark Price: ${price:,.2f}")
                return price
            else:
                logger.warning(f"⚠️  No price field in orderbook: {list(ob.keys())}")
                # Try to get from order_book field if it exists
                if 'order_book' in ob and 'bids' in ob['order_book'] and 'asks' in ob['order_book']:
                    bids = ob['order_book']['bids']
                    asks = ob['order_book']['asks']
                    if bids and asks:
                        best_bid = float(bids[0]['price'])
                        best_ask = float(asks[0]['price'])
                        mid_price = (best_bid + best_ask) / 2
                        logger.debug(f"📊 Mid Price: ${mid_price:,.2f}")
                        return mid_price
                return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get price: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_best_ask_bid(self, market_id: int) -> tuple[Optional[float], Optional[float]]:
        """Get best ask and bid prices from orderbook"""
        try:
            orderbook_data = await self.api_wrapper.get_orderbook(market_id)
            
            if orderbook_data and 'order_book_details' in orderbook_data:
                ob = orderbook_data['order_book_details'][0]
                
                best_ask = float(ob.get('best_ask_price', 0))
                best_bid = float(ob.get('best_bid_price', 0))
                
                if best_ask > 0 and best_bid > 0:
                    logger.debug(f"📊 Best Ask: ${best_ask:,.2f} | Best Bid: ${best_bid:,.2f}")
                    return (best_ask, best_bid)
            
            return (None, None)
            
        except Exception as e:
            logger.error(f"Error getting best ask/bid: {e}")
            return (None, None)
    
    async def determine_position_side(self, market_id: str) -> str:
        """
        Determine whether to go LONG or SHORT
        You can implement your own logic here (trend detection, etc.)
        For now, we'll use a simple random/alternating approach
        """
        # TODO: Implement your preferred entry logic
        # Options:
        # 1. Trend following (if price > MA, go long)
        # 2. Mean reversion (if price too high, go short)
        # 3. Random (for testing)
        # 4. Always long (bullish bias)
        
        # Using SHORT because LONG orders aren't filling on Lighter
        # (LONG orders get 200 OK but are cancelled, SHORT orders work)
        return 'short'
    
    async def place_market_order(self, market_id: int, side: str, size: float) -> Optional[dict]:
        """Place a market order using Lighter SDK"""
        try:
            import lighter
            import time
            
            logger.info(f"📤 Placing {side.upper()} market order...")
            logger.info(f"   Market ID: {market_id} | Size: {size:.8f} BTC")
            
            # Get current price
            current_price = await self.get_current_price(market_id)
            if not current_price:
                logger.error("Cannot get current price")
                return None
            
            # Calculate order parameters
            position_size_btc = size  # BTC amount to trade
            base_amount = int(position_size_btc * 1e8)  # Convert to satoshis
            
            # Get best bid/ask for price
            wrapper = self.api_wrapper
            orderbook = await wrapper.get_orderbook(market_id)
            
            if orderbook and 'order_book_details' in orderbook:
                btc_data = orderbook['order_book_details'][0]
                best_bid = float(btc_data.get('best_bid_price', current_price))
                best_ask = float(btc_data.get('best_ask_price', current_price))
            else:
                best_bid = current_price
                best_ask = current_price
            
            # For SHORT (sell): use best_bid, for LONG (buy): use best_ask
            if side.lower() == 'short':
                is_ask = True  # SELL
                avg_execution_price = int(best_bid)
                logger.info(f"   SHORT: Selling at best bid ${best_bid:,.2f}")
            else:
                is_ask = False  # BUY
                avg_execution_price = int(best_ask)
                logger.info(f"   LONG: Buying at best ask ${best_ask:,.2f}")
            
            # Generate unique client order index
            client_order_index = int(time.time() * 1000) % 2147483647
            
            logger.info(f"   Position Size: {position_size_btc:.8f} BTC = {base_amount} satoshis")
            logger.info(f"   Current Price: ${current_price:,.2f}")
            logger.info(f"   Execution Price: ${avg_execution_price:,}")
            logger.info(f"   is_ask: {is_ask}")
            logger.info(f"   client_order_index: {client_order_index}")
            
            # Place the order
            order_result, tx_hash, order_id = await self.client.create_market_order(
                market_index=market_id,
                client_order_index=client_order_index,
                base_amount=base_amount,
                avg_execution_price=avg_execution_price,
                is_ask=is_ask,
                reduce_only=False
            )
            
            logger.info(f"✅ Order placed! TX: {tx_hash}, Order ID: {order_id}")
            
            return {
                'order_id': order_id,
                'tx_hash': tx_hash,
                'market_id': market_id,
                'side': side,
                'size': size,
                'entry_price': current_price
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to place order: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def close_position_order(self, market_id: int, reason: str = "manual"):
        """Close current position by placing opposite order"""
        if not self.current_position:
            logger.warning("No position to close")
            return False
        
        try:
            logger.info(f"\n🔴 CLOSING POSITION ({reason})")
            logger.info("=" * 70)
            
            # Get current price for P&L
            current_price = await self.get_current_price(market_id)
            if not current_price:
                logger.error("Cannot get current price")
                return False
            
            # Calculate P&L
            entry_price = self.entry_price
            position_size = self.position_size
            side = self.current_side
            
            if side == 'long':
                pnl_percent = ((current_price - entry_price) / entry_price) * 100
            else:
                pnl_percent = ((entry_price - current_price) / entry_price) * 100
            
            logger.info(f"   Entry: ${entry_price:.2f} | Exit: ${current_price:.2f}")
            logger.info(f"   P&L: {pnl_percent:+.2f}%")
            
            if not self.config.get('trading_enabled', False):
                logger.warning("⚠️  PAPER TRADING - Simulated close")
            else:
                # Place opposite order to close
                close_side = 'short' if side == 'long' else 'long'
                
                order_result = await self.place_market_order(
                    market_id=market_id,
                    side=close_side,
                    size=position_size
                )
                
                if not order_result:
                    logger.error("❌ Failed to close position!")
                    return False
                
                logger.info("✅ Position closed!")
            
            # Reset tracking
            self.current_position = None
            self.entry_price = None
            self.position_size = None
            self.current_side = None
            self.has_doubled = False
            self.highest_profit = 0
            self.current_stop_loss = None
            self.last_stop_loss_time = datetime.now()
            
            logger.info("=" * 70 + "\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error closing position: {e}")
            return False
    
    async def open_new_position(self, market_id: int):
        """Open a new position"""
        logger.info("\n" + "=" * 70)
        logger.info("📤 OPENING NEW POSITION")
        logger.info("=" * 70)
        
        # Get current price
        current_price = await self.get_current_price(market_id)
        if not current_price:
            logger.error("Cannot get current price")
            return
        
        # Get account balance
        balance = await self.get_account_balance()
        if balance <= 0:
            logger.error("Insufficient balance")
            return
        
        # Calculate position size - 5% THAT WORKED!
        # 5% of balance × 50x leverage = position value
        position_percent = self.position_size_percent  # 0.05 = 5%
        leverage = 50  # 50x leverage
        
        margin_value = balance * position_percent
        total_position_value = margin_value * leverage
        position_size_btc = total_position_value / current_price
        
        # Determine side
        side = await self.determine_position_side(market_id)
        
        logger.info(f"💰 Balance: ${balance:.2f}")
        logger.info(f"📊 Current Price: ${current_price:.2f}")
        logger.info(f"💵 Margin: ${margin_value:.2f} ({position_percent*100}% of balance)")
        logger.info(f"⚡ Leverage: {leverage}x")
        logger.info(f"📈 Total Position: ${total_position_value:.2f}")
        logger.info(f"📊 Position Size: {position_size_btc:.8f} BTC")
        logger.info(f"{'🟢 LONG' if side == 'long' else '🔴 SHORT'}")
        
        if not self.config.get('trading_enabled', False):
            logger.warning("⚠️  PAPER TRADING MODE - No real order placed")
            # Simulate position for testing
            self.current_position = {
                'id': f'paper_{datetime.now().timestamp()}',
                'market': market_id,
                'side': side,
                'size': position_size_btc,
                'entry_price': current_price,
                'leverage': self.leverage
            }
        else:
            # Place actual order via Lighter SDK
            logger.info("📤 Placing REAL order...")
            
            order_result = await self.place_market_order(
                market_id=market_id,
                side=side,
                size=position_size_btc
            )
            
            if not order_result:
                logger.error("❌ Failed to place order!")
                return
            
            self.current_position = order_result
        
        # Initialize tracking
        self.entry_price = current_price
        self.position_size = position_size_btc
        self.current_side = side
        self.has_doubled = False
        self.highest_profit = 0
        self.current_stop_loss = None
        
        logger.info("✅ Position opened successfully!")
        logger.info("=" * 70 + "\n")
    
    async def monitor_position(self, market_id: int):
        """Monitor and manage existing position"""
        # Get current price
        current_price = await self.get_current_price(market_id)
        if not current_price:
            return
        
        # Calculate P&L percentage
        if self.current_side == 'long':
            pnl_percent = ((current_price - self.entry_price) / self.entry_price) * 100
        else:  # short
            pnl_percent = ((self.entry_price - current_price) / self.entry_price) * 100
        
        # Apply leverage multiplier
        leveraged_pnl = pnl_percent * self.leverage
        
        # Update highest profit
        if leveraged_pnl > self.highest_profit:
            self.highest_profit = leveraged_pnl
        
        # Display current status
        pnl_color = "🟢" if leveraged_pnl >= 0 else "🔴"
        logger.info(f"{pnl_color} Position P&L: {leveraged_pnl:.2f}% | "
                   f"Entry: ${self.entry_price:.2f} | "
                   f"Current: ${current_price:.2f} | "
                   f"Stop Loss: {self.current_stop_loss if self.current_stop_loss else 'None'}")
        
        # Check for double down opportunity
        if leveraged_pnl <= self.double_down_threshold and not self.has_doubled:
            await self.double_position(market_id, current_price)
            return
        
        # Update trailing stop loss
        await self.update_trailing_stop(leveraged_pnl)
        
        # Check stop loss
        if self.current_stop_loss and leveraged_pnl <= self.current_stop_loss:
            await self.trigger_stop_loss(market_id, current_price, leveraged_pnl)
    
    async def update_trailing_stop(self, current_pnl: float):
        """Update trailing stop loss based on profit thresholds"""
        for threshold in self.profit_thresholds:
            if current_pnl >= threshold:
                new_stop_loss = threshold - self.stop_loss_offset
                
                # Only update if new stop loss is higher than current
                if self.current_stop_loss is None or new_stop_loss > self.current_stop_loss:
                    old_stop = self.current_stop_loss
                    self.current_stop_loss = new_stop_loss
                    logger.info(f"📈 Trailing stop updated: {old_stop} → {new_stop_loss}%")
                    logger.info(f"   Current profit: {current_pnl:.2f}%")
                    logger.info(f"   Locked in minimum: {new_stop_loss}%")
    
    async def double_position(self, market_id: str, current_price: float):
        """Double the position size (Martingale)"""
        logger.warning("\n" + "⚠️ " * 35)
        logger.warning("🔥 DOUBLING POSITION (MARTINGALE)")
        logger.warning("⚠️ " * 35)
        
        logger.info(f"📉 Position at {self.double_down_threshold}% loss")
        logger.info(f"💰 Current Price: ${current_price:.2f}")
        logger.info(f"📊 Original Entry: ${self.entry_price:.2f}")
        logger.info(f"🔄 Doubling position size...")
        
        if not self.config.get('trading_enabled', False):
            logger.warning("⚠️  PAPER TRADING MODE - Simulating double down")
            # Update average entry price
            total_size = self.position_size * 2
            avg_price = (self.entry_price * self.position_size + current_price * self.position_size) / total_size
            
            self.position_size = total_size
            self.entry_price = avg_price
            self.has_doubled = True
            
            logger.info(f"✅ Position doubled!")
            logger.info(f"   New Size: {self.position_size:.6f}")
            logger.info(f"   New Avg Entry: ${self.entry_price:.2f}")
        else:
            # Place actual double down order
            logger.info("📤 Placing double down order...")
            try:
                # TODO: Implement actual order placement
                logger.warning("⚠️  Order placement not yet implemented in SDK")
            except Exception as e:
                logger.error(f"❌ Failed to double position: {e}")
        
        logger.warning("⚠️ " * 35 + "\n")
    
    async def trigger_stop_loss(self, market_id: int, current_price: float, final_pnl: float):
        """Trigger stop loss and close position"""
        logger.warning("\n" + "🛑 " * 35)
        logger.warning("STOP LOSS TRIGGERED!")
        logger.warning("🛑 " * 35)
        
        logger.info(f"📉 Final P&L: {final_pnl:.2f}%")
        logger.info(f"🏆 Highest Profit Reached: {self.highest_profit:.2f}%")
        
        # Close position using our close_position_order function
        await self.close_position_order(market_id, reason="stop_loss")
        
        logger.info(f"⏸️  Entering cooldown for {self.cooldown_seconds}s...")
        logger.warning("🛑 " * 35 + "\n")
    
    def get_stats(self) -> Dict:
        """Get strategy statistics"""
        return {
            'position_active': self.current_position is not None,
            'entry_price': self.entry_price,
            'current_side': self.current_side,
            'position_size': self.position_size,
            'has_doubled': self.has_doubled,
            'highest_profit': self.highest_profit,
            'current_stop_loss': self.current_stop_loss,
            'in_cooldown': self.is_in_cooldown()
        }
