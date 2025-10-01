#!/usr/bin/env python3
"""
Configuration for Aggressive Leverage Strategy
"""

# ========================================
# ⚠️  EXTREMELY HIGH RISK STRATEGY! ⚠️
# ========================================

# Trading Settings
TRADING_ENABLED = True  # Testing again

# Market to trade
MARKET_ID = 1  # BTC market (1=BTC, 2=SOL, etc.)
MARKET = 'BTC'  # Display name

# ========================================
# STRATEGY PARAMETERS
# ========================================

AGGRESSIVE_STRATEGY_CONFIG = {
    # Position sizing
    # Using EXACT calculation from test_short_order.py that worked
    # 5% margin × 50x leverage = position value
    # Example: 5% of $104.91 = $5.25 × 50 = $262.50 position
    'position_size_percent': 0.05,   # 5% of balance as margin
    
    # Leverage (NOT used in calculation - just for display/reference)
    'leverage': 50,                  # Your Lighter UI leverage setting (informational only)
    
    # Trailing stop loss thresholds
    'profit_thresholds': [
        2,   # At +2% profit → stop loss at +1%
        3,   # At +3% profit → stop loss at +2%
        4,   # At +4% profit → stop loss at +3%
        5,   # At +5% profit → stop loss at +4%
        6,   # At +6% profit → stop loss at +5%
        7,   # At +7% profit → stop loss at +6%
        8,   # At +8% profit → stop loss at +7%
        9,   # At +9% profit → stop loss at +8%
        10,  # At +10% profit → stop loss at +9%
        15,  # At +15% profit → stop loss at +14%
        20,  # At +20% profit → stop loss at +19%
    ],
    
    # Double down (Martingale)
    'double_down_threshold': -6,     # Double position at -6% loss
    
    # Timing
    'cooldown_seconds': 60,          # Wait 60s after stop loss before new position
    'check_interval': 5,             # Check position every 5 seconds
    
    # Safety limits (IMPORTANT!)
    'max_loss_per_day': 0.20,        # Stop trading if 20% daily loss
    'max_consecutive_losses': 5,     # Stop after 5 consecutive losses
    
    # Enable trading
    'trading_enabled': TRADING_ENABLED,
}

# ========================================
# POSITION ENTRY LOGIC
# ========================================

ENTRY_LOGIC = 'trend_following'  # Options: 'trend_following', 'random', 'always_long', 'always_short'

# For trend following
TREND_CONFIG = {
    'ma_period': 20,                 # Moving average period
    'trend_threshold': 0.01,         # 1% above MA = uptrend
}

# ========================================
# RISK WARNINGS
# ========================================

RISK_WARNINGS = """
⚠️  EXTREME RISK WARNING ⚠️

This strategy is EXTREMELY RISKY:

1. 50x LEVERAGE:
   - A 2% move against you = 100% position loss
   - Can be liquidated very quickly
   - Total account loss possible

2. MARTINGALE (DOUBLING):
   - Doubling losing positions can lead to massive losses
   - Can drain account very quickly
   - Not recommended for most traders

3. HIGH FREQUENCY:
   - Checking every 5 seconds
   - Quick position changes
   - Requires constant monitoring

4. RECOMMENDED PRECAUTIONS:
   - Start with VERY small amounts
   - Test in paper mode extensively
   - Never use more than you can afford to lose completely
   - Set strict daily loss limits
   - Monitor constantly
   - Have a plan to stop

5. NOT SUITABLE FOR:
   - Beginners
   - Risk-averse traders
   - Accounts you can't afford to lose
   - Unmonitored trading

USE AT YOUR OWN RISK!
Only enable after understanding all risks.
"""

def display_risks():
    """Display risk warnings"""
    print("\n" + "=" * 70)
    print(RISK_WARNINGS)
    print("=" * 70 + "\n")

def validate_config():
    """Validate configuration and display warnings"""
    print("⚙️  Configuration:")
    print(f"   Market: {MARKET}")
    print(f"   Position Size: {AGGRESSIVE_STRATEGY_CONFIG['position_size_percent']*100}%")
    print(f"   Leverage: {AGGRESSIVE_STRATEGY_CONFIG['leverage']}x")
    print(f"   Double Down at: {AGGRESSIVE_STRATEGY_CONFIG['double_down_threshold']}%")
    print(f"   Trading Enabled: {TRADING_ENABLED}")
    print()
    
    if TRADING_ENABLED:
        print("⚠️  LIVE TRADING ENABLED - REAL MONEY AT RISK!")
        print()
    else:
        print("ℹ️  Paper trading mode (safe)")
    
    return True

if __name__ == "__main__":
    if validate_config():
        print("✅ Configuration validated")
    else:
        print("❌ Configuration cancelled")
