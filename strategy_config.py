#!/usr/bin/env python3
"""
Strategy Configuration
Define your trading strategy parameters here
"""

# ========================================
# GENERAL SETTINGS
# ========================================

TRADING_ENABLED = False  # Set to True to enable live trading
STRATEGY = 'momentum'  # Choose: 'market_maker', 'momentum', 'grid', 'arbitrage'

# Markets to trade
MARKETS = [
    'BTC-USD',
    'ETH-USD',
    # Add more markets here
]

# ========================================
# RISK MANAGEMENT
# ========================================

RISK_MANAGEMENT = {
    'max_position_size': 1.0,        # Maximum position size
    'max_loss_per_trade': 0.02,      # 2% max loss per trade
    'max_daily_loss': 0.05,          # 5% max daily loss
    'stop_loss_percent': 0.03,       # 3% stop loss
    'take_profit_percent': 0.06,     # 6% take profit
}

# ========================================
# MARKET MAKER STRATEGY
# ========================================

MARKET_MAKER_CONFIG = {
    'spread': 0.002,              # 0.2% spread (distance from mid price)
    'order_size': 0.01,           # Size per order
    'max_position': 0.1,          # Maximum total position
    'interval': 10,               # Update interval in seconds
    'num_levels': 3,              # Number of price levels
    'level_spacing': 0.001,       # 0.1% spacing between levels
}

# ========================================
# MOMENTUM STRATEGY
# ========================================

MOMENTUM_CONFIG = {
    'lookback_period': 20,        # Number of periods to look back
    'threshold': 0.02,            # 2% price move to trigger
    'position_size': 0.1,         # Position size as fraction of balance
    'interval': 60,               # Check interval in seconds
    'min_volume': 1000,           # Minimum volume to consider
    'exit_threshold': 0.01,       # 1% to exit position
}

# ========================================
# GRID TRADING STRATEGY
# ========================================

GRID_CONFIG = {
    'grid_levels': 10,            # Total number of grid levels
    'grid_spacing': 0.01,         # 1% spacing between levels
    'order_size': 0.01,           # Size per grid order
    'base_price': None,           # None = use current price
    'interval': 30,               # Check interval in seconds
    'reset_on_fill': True,        # Reset grid when order fills
}

# ========================================
# ARBITRAGE STRATEGY
# ========================================

ARBITRAGE_CONFIG = {
    'min_profit': 0.005,          # 0.5% minimum profit
    'markets': [                  # Markets to monitor
        'BTC-USD',
        'BTC-USDT',
    ],
    'max_position': 0.5,          # Maximum position per trade
    'interval': 5,                # Scan interval in seconds
    'include_fees': True,         # Consider trading fees
}

# ========================================
# ADVANCED SETTINGS
# ========================================

ADVANCED = {
    # Slippage tolerance
    'max_slippage': 0.005,        # 0.5% max slippage
    
    # Order management
    'order_timeout': 300,         # Cancel orders after 5 minutes
    'max_retries': 3,             # Max retries for failed orders
    
    # Monitoring
    'log_level': 'INFO',          # DEBUG, INFO, WARNING, ERROR
    'save_trades': True,          # Save trade history to file
    'trade_log_file': 'trades.csv',
    
    # Notifications (optional)
    'enable_notifications': False,
    'notify_on_trade': True,
    'notify_on_error': True,
}

# ========================================
# BACKTESTING (Coming Soon)
# ========================================

BACKTEST = {
    'enabled': False,
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'initial_balance': 10000,
}

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_strategy_config(strategy_name: str) -> dict:
    """Get configuration for a specific strategy"""
    configs = {
        'market_maker': MARKET_MAKER_CONFIG,
        'momentum': MOMENTUM_CONFIG,
        'grid': GRID_CONFIG,
        'arbitrage': ARBITRAGE_CONFIG,
    }
    return configs.get(strategy_name, {})


def validate_config():
    """Validate configuration"""
    errors = []
    
    # Check if strategy exists
    valid_strategies = ['market_maker', 'momentum', 'grid', 'arbitrage']
    if STRATEGY not in valid_strategies:
        errors.append(f"Invalid strategy: {STRATEGY}. Must be one of {valid_strategies}")
    
    # Check markets
    if not MARKETS:
        errors.append("No markets configured")
    
    # Check risk management
    if RISK_MANAGEMENT['max_loss_per_trade'] > 0.1:
        errors.append("Warning: max_loss_per_trade > 10% is very risky")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    print("✅ Configuration validated")
    return True


# Validate on import
if __name__ == "__main__":
    validate_config()
