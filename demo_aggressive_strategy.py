#!/usr/bin/env python3
"""
Demo of Your Aggressive 50x Leverage Strategy
Shows how the strategy works with simulated price movements
"""

import asyncio
import random
from datetime import datetime

class AggressiveStrategyDemo:
    """Demo your exact strategy with simulated prices"""
    
    def __init__(self):
        self.position_size_percent = 0.05  # 5%
        self.leverage = 50  # 50x
        self.balance = 1000  # $1000 starting balance
        self.entry_price = None
        self.position_size = None
        self.current_side = 'long'
        self.has_doubled = False
        self.highest_profit = 0
        self.current_stop_loss = None
        self.trade_count = 0
        self.wins = 0
        self.losses = 0
        
    def get_simulated_price(self, base_price, volatility=0.002):
        """Simulate price movement"""
        change = random.uniform(-volatility, volatility)
        return base_price * (1 + change)
    
    def calculate_pnl(self, current_price):
        """Calculate P&L percentage"""
        if not self.entry_price:
            return 0
        
        if self.current_side == 'long':
            pnl = ((current_price - self.entry_price) / self.entry_price) * 100
        else:
            pnl = ((self.entry_price - current_price) / self.entry_price) * 100
        
        return pnl * self.leverage  # Apply leverage
    
    def update_trailing_stop(self, pnl):
        """Update trailing stop loss"""
        thresholds = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for threshold in thresholds:
            if pnl >= threshold:
                new_stop = threshold - 1
                if self.current_stop_loss is None or new_stop > self.current_stop_loss:
                    old_stop = self.current_stop_loss
                    self.current_stop_loss = new_stop
                    print(f"   📈 Trailing stop updated: {old_stop} → {new_stop}%")
                    print(f"      Locked in minimum profit: +{new_stop}%")
                    return True
        return False
    
    async def run_demo(self, num_trades=5):
        """Run demo of the strategy"""
        print("\n" + "=" * 70)
        print("⚡ AGGRESSIVE 50X LEVERAGE STRATEGY DEMO")
        print("=" * 70)
        print(f"\n💰 Starting Balance: ${self.balance:.2f}")
        print(f"📊 Position Size: {self.position_size_percent*100}% = ${self.balance * self.position_size_percent:.2f}")
        print(f"⚡ Leverage: {self.leverage}x")
        print(f"💵 Total Exposure per trade: ${self.balance * self.position_size_percent * self.leverage:.2f}")
        print("\n" + "=" * 70)
        
        for trade_num in range(1, num_trades + 1):
            print(f"\n{'='*70}")
            print(f"TRADE #{trade_num}")
            print("=" * 70)
            
            # Open position
            self.entry_price = 50000 + random.uniform(-1000, 1000)
            self.position_size = (self.balance * self.position_size_percent * self.leverage) / self.entry_price
            self.current_side = random.choice(['long', 'short'])
            self.has_doubled = False
            self.highest_profit = 0
            self.current_stop_loss = None
            
            print(f"\n📤 OPENING POSITION")
            print(f"   Direction: {'🟢 LONG' if self.current_side == 'long' else '🔴 SHORT'}")
            print(f"   Entry Price: ${self.entry_price:.2f}")
            print(f"   Position Size: {self.position_size:.6f} BTC")
            print(f"   Exposure: ${self.position_size * self.entry_price:.2f}")
            
            # Simulate price movements
            current_price = self.entry_price
            steps = random.randint(10, 30)
            
            for step in range(steps):
                await asyncio.sleep(0.2)  # Faster for demo
                
                # Simulate price movement
                current_price = self.get_simulated_price(current_price, volatility=0.001)
                pnl = self.calculate_pnl(current_price)
                
                if pnl > self.highest_profit:
                    self.highest_profit = pnl
                
                # Display status
                pnl_color = "🟢" if pnl >= 0 else "🔴"
                print(f"\r   {pnl_color} P&L: {pnl:+.2f}% | Price: ${current_price:.2f} | Stop: {self.current_stop_loss if self.current_stop_loss else 'None'} | Highest: {self.highest_profit:.2f}%", end='', flush=True)
                
                # Check for double down
                if pnl <= -6 and not self.has_doubled:
                    print(f"\n\n   ⚠️  DOUBLING POSITION (Martingale)")
                    print(f"   📉 Hit -6% threshold")
                    print(f"   🔄 Doubling position size...")
                    
                    # Average down
                    total_size = self.position_size * 2
                    avg_price = (self.entry_price * self.position_size + current_price * self.position_size) / total_size
                    self.position_size = total_size
                    self.entry_price = avg_price
                    self.has_doubled = True
                    
                    print(f"   ✅ New Average Entry: ${self.entry_price:.2f}")
                    print(f"   📊 New Position Size: {self.position_size:.6f} BTC")
                    
                    # Recalculate P&L
                    pnl = self.calculate_pnl(current_price)
                    continue
                
                # Update trailing stop
                if pnl > 0:
                    if self.update_trailing_stop(pnl):
                        pass  # Stop updated
                
                # Check stop loss
                if self.current_stop_loss and pnl <= self.current_stop_loss:
                    print(f"\n\n   🛑 STOP LOSS TRIGGERED!")
                    print(f"   📊 Entry: ${self.entry_price:.2f}")
                    print(f"   💰 Exit: ${current_price:.2f}")
                    print(f"   📉 Final P&L: {pnl:+.2f}%")
                    
                    # Calculate dollar P&L
                    position_value = self.balance * self.position_size_percent
                    dollar_pnl = position_value * (pnl / 100)
                    self.balance += dollar_pnl
                    
                    print(f"   💵 Dollar P&L: ${dollar_pnl:+.2f}")
                    print(f"   💰 New Balance: ${self.balance:.2f}")
                    
                    self.trade_count += 1
                    if pnl > 0:
                        self.wins += 1
                        print(f"   ✅ WIN #{self.wins}")
                    else:
                        self.losses += 1
                        print(f"   ❌ LOSS #{self.losses}")
                    
                    break
            
            print(f"\n   ⏸️  Cooldown period (60s)...")
            await asyncio.sleep(1)  # Shortened for demo
        
        # Final summary
        print(f"\n\n{'='*70}")
        print("📊 FINAL RESULTS")
        print("=" * 70)
        print(f"Starting Balance: $1000.00")
        print(f"Final Balance: ${self.balance:.2f}")
        print(f"Total P&L: ${self.balance - 1000:+.2f} ({((self.balance/1000)-1)*100:+.2f}%)")
        print(f"Trades: {self.trade_count}")
        print(f"Wins: {self.wins}")
        print(f"Losses: {self.losses}")
        if self.trade_count > 0:
            print(f"Win Rate: {(self.wins/self.trade_count)*100:.1f}%")
        print("=" * 70)

async def main():
    demo = AggressiveStrategyDemo()
    await demo.run_demo(num_trades=3)  # Run 3 trades as demo
    
    print("\n✨ This demonstrates YOUR exact strategy!")
    print("\nStrategy features shown:")
    print("✅ 5% position size with 50x leverage")
    print("✅ Trailing stop loss (updates as profit grows)")
    print("✅ Martingale doubling at -6%")
    print("✅ Automatic position management")
    print("\n⚠️  Remember: This is a DEMO with simulated data!")
    print("Real trading has:")
    print("  • Actual market volatility")
    print("  • Slippage and fees")
    print("  • Liquidation risk")
    print("  • Much higher stress!")

if __name__ == "__main__":
    asyncio.run(main())

