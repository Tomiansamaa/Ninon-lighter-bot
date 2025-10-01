# 📈 Lighter Trading Bot - Trading Guide

## 🎯 Overview

Your Lighter trading bot now has **4 complete trading strategies**:

1. **Market Maker** - Provides liquidity and earns the spread
2. **Momentum** - Follows price trends and momentum
3. **Grid Trading** - Places orders at regular price intervals
4. **Arbitrage** - Exploits price differences between markets

---

## 🚀 Quick Start

### 1. Configure Your Strategy

Edit `strategy_config.py`:

```python
# Choose your strategy
STRATEGY = 'momentum'  # or 'market_maker', 'grid', 'arbitrage'

# Enable paper trading first!
TRADING_ENABLED = False  # Set to True for live trading

# Select markets
MARKETS = ['BTC-USD', 'ETH-USD']
```

### 2. Test in Paper Mode

```bash
python3 trading_bot_main.py
```

This runs without placing real orders.

### 3. Enable Live Trading

When ready:

```python
TRADING_ENABLED = True  # in strategy_config.py
```

⚠️ **Warning**: Only enable after thorough testing!

---

## 📊 Trading Strategies Explained

### 1️⃣ Market Maker Strategy

**How it works:**
- Places buy orders below market price
- Places sell orders above market price
- Profits from the spread between orders

**Configuration:**
```python
MARKET_MAKER_CONFIG = {
    'spread': 0.002,          # 0.2% spread
    'order_size': 0.01,       # Size per order
    'max_position': 0.1,      # Max total position
    'interval': 10,           # Update every 10 seconds
}
```

**Best for:**
- Stable, liquid markets
- Earning consistent small profits
- 24/7 automated trading

**Risk:** Low to medium

---

### 2️⃣ Momentum Strategy

**How it works:**
- Tracks price movements over time
- Buys when price is trending up
- Sells when price is trending down

**Configuration:**
```python
MOMENTUM_CONFIG = {
    'lookback_period': 20,    # Look at last 20 periods
    'threshold': 0.02,        # 2% move triggers trade
    'position_size': 0.1,     # 10% of balance per trade
    'interval': 60,           # Check every 60 seconds
}
```

**Best for:**
- Trending markets
- Medium-term holds
- Capturing larger moves

**Risk:** Medium

---

### 3️⃣ Grid Trading Strategy

**How it works:**
- Places buy and sell orders at fixed intervals
- Profits from price oscillations
- Automatically rebalances

**Configuration:**
```python
GRID_CONFIG = {
    'grid_levels': 10,        # 10 total levels
    'grid_spacing': 0.01,     # 1% between levels
    'order_size': 0.01,       # Size per level
    'base_price': None,       # Use current price
}
```

**Best for:**
- Range-bound markets
- Sideways price action
- Automated rebalancing

**Risk:** Medium to high

---

### 4️⃣ Arbitrage Strategy

**How it works:**
- Monitors multiple markets
- Buys in one market, sells in another
- Profits from price differences

**Configuration:**
```python
ARBITRAGE_CONFIG = {
    'min_profit': 0.005,      # 0.5% minimum profit
    'markets': [
        'BTC-USD',
        'BTC-USDT',
    ],
    'interval': 5,            # Fast scanning
}
```

**Best for:**
- Multi-market access
- Very fast execution
- Low-risk profits

**Risk:** Low (if executed quickly)

---

## 🛡️ Risk Management

All strategies include built-in risk management:

```python
RISK_MANAGEMENT = {
    'max_position_size': 1.0,      # Max position
    'max_loss_per_trade': 0.02,    # 2% stop loss
    'max_daily_loss': 0.05,        # 5% daily limit
}
```

### Risk Controls:

1. **Position Limits** - Caps maximum exposure
2. **Stop Loss** - Automatically exits losing trades
3. **Daily Loss Limit** - Stops trading if daily loss exceeded
4. **Slippage Control** - Prevents bad fills

---

## 📝 Configuration Examples

### Conservative Setup (Low Risk)

```python
STRATEGY = 'market_maker'

MARKET_MAKER_CONFIG = {
    'spread': 0.005,          # 0.5% spread (wider)
    'order_size': 0.005,      # Small orders
    'max_position': 0.05,     # Small max position
}

RISK_MANAGEMENT = {
    'max_loss_per_trade': 0.01,    # 1% stop loss
    'max_daily_loss': 0.03,        # 3% daily limit
}
```

### Aggressive Setup (Higher Risk)

```python
STRATEGY = 'momentum'

MOMENTUM_CONFIG = {
    'threshold': 0.015,       # 1.5% trigger (more trades)
    'position_size': 0.2,     # Larger positions
}

RISK_MANAGEMENT = {
    'max_loss_per_trade': 0.03,    # 3% stop loss
    'max_daily_loss': 0.10,        # 10% daily limit
}
```

### Multi-Market Setup

```python
STRATEGY = 'arbitrage'

MARKETS = [
    'BTC-USD',
    'BTC-USDT',
    'ETH-USD',
    'ETH-USDT',
]

ARBITRAGE_CONFIG = {
    'min_profit': 0.003,      # 0.3% minimum
    'interval': 2,            # Check every 2 seconds
}
```

---

## 🔄 Workflow

### Development Workflow:

1. **Configure** → Edit `strategy_config.py`
2. **Paper Test** → Run with `TRADING_ENABLED = False`
3. **Monitor** → Watch logs for 24-48 hours
4. **Analyze** → Review performance in `trades.csv`
5. **Optimize** → Adjust parameters
6. **Live Test** → Enable with small position sizes
7. **Scale Up** → Gradually increase sizes

---

## 📊 Monitoring & Logs

### Real-Time Monitoring

The bot logs all activity:

```bash
# Watch logs in real-time
tail -f trading_bot.log
```

### Trade History

All trades saved to `trades.csv`:
- Timestamp
- Market
- Side (buy/sell)
- Price
- Size
- P&L

### Performance Metrics

Monitor:
- Daily P&L
- Win rate
- Average profit/loss
- Max drawdown

---

## ⚙️ Advanced Configuration

### Custom Strategy Parameters

You can fine-tune each strategy:

```python
# Market Maker: Multi-level quotes
MARKET_MAKER_CONFIG = {
    'num_levels': 5,          # 5 price levels
    'level_spacing': 0.001,   # 0.1% between levels
    'order_size': 0.02,       # Size increases per level
}

# Momentum: Multiple timeframes
MOMENTUM_CONFIG = {
    'short_period': 5,        # Fast signal
    'long_period': 20,        # Slow signal
    'volume_filter': True,    # Require volume confirmation
}
```

### Notifications (Coming Soon)

```python
ADVANCED = {
    'enable_notifications': True,
    'notify_on_trade': True,
    'notify_on_error': True,
    'notify_on_profit': 0.05,  # Notify on 5%+ profit
}
```

---

## 🚨 Safety Checklist

Before enabling live trading:

- [ ] Tested in paper mode for 24+ hours
- [ ] Reviewed and understood the strategy
- [ ] Set appropriate position sizes
- [ ] Configured stop losses
- [ ] Set daily loss limits
- [ ] Have sufficient account balance
- [ ] Understand the risks involved
- [ ] Can monitor the bot regularly

---

## 🐛 Troubleshooting

### Bot Not Placing Orders

1. Check `TRADING_ENABLED = True`
2. Verify account has sufficient balance
3. Check market is active
4. Review logs for errors

### Strategy Not Profitable

1. Backtest with different parameters
2. Check market conditions match strategy
3. Reduce position sizes
4. Adjust thresholds

### High Losses

1. Immediately stop the bot
2. Review risk management settings
3. Check if stop losses are working
4. Reduce position sizes before restarting

---

## 📚 Strategy Selection Guide

| Market Condition | Best Strategy | Risk Level |
|-----------------|---------------|------------|
| Trending Up/Down | Momentum | Medium |
| Sideways Range | Grid Trading | Medium |
| High Volatility | Market Maker | Low-Med |
| Multiple Markets | Arbitrage | Low |
| Stable/Liquid | Market Maker | Low |

---

## 🎓 Learning Resources

### Recommended Reading:

1. **Market Making**: Study bid-ask spread and liquidity provision
2. **Technical Analysis**: Learn indicators and chart patterns
3. **Risk Management**: Position sizing and Kelly criterion
4. **Backtesting**: Historical testing methodologies

### Practice:

1. Start with paper trading
2. Use small position sizes
3. Monitor for at least 1 week
4. Gradually scale up

---

## 📞 Support

- **Documentation**: Check all `.md` files in project
- **Lighter Docs**: https://apidocs.lighter.xyz/docs
- **Logs**: Review `trading_bot.log` for errors
- **Configuration**: Double-check `strategy_config.py`

---

## ⚠️ Disclaimer

**Important**: 
- Trading involves significant risk
- Past performance doesn't guarantee future results
- Only trade with money you can afford to lose
- This bot is for educational purposes
- Always test thoroughly before live trading
- You are responsible for your trading decisions

---

**Happy Trading!** 📈🚀

Start with paper trading, understand the strategies, and scale gradually.

*Last Updated: September 29, 2025*
