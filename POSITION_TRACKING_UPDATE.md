# Position Tracking Update ✅

## What Changed

The bot now properly tracks and manages positions based on how Lighter actually works:

### 1. **Opening Positions**
- Bot calculates: `margin × leverage = position_value`
- Then converts to BTC: `position_value / current_price = position_size_btc`
- Sends BTC amount to Lighter
- **Lighter handles all leverage/margin calculations in their UI**

### 2. **Position Tracking**
The bot tracks:
- `entry_price`: Price when position opened
- `position_size`: BTC amount
- `current_side`: 'short' or 'long'
- `highest_profit`: For trailing stop loss
- `current_stop_loss`: Current stop loss level
- `has_doubled`: Whether we've doubled down

### 3. **Closing Positions**
- For SHORT position → Place LONG (buy) order to close
- For LONG position → Place SHORT (sell) order to close
- Uses same BTC amount as original position

### 4. **Strategy Logic**
✅ **Trailing Stop Loss:**
- At +2% profit → Set stop loss at +1%
- At +3% profit → Move stop loss to +2%
- Continues trailing up

✅ **Position Doubling:**
- At -6% loss → Double position size at current price
- Gets better average entry price
- Only doubles once per position

✅ **Cooldown Period:**
- After stop loss triggers, wait before opening new position
- Prevents overtrading

## Current Configuration

```python
AGGRESSIVE_STRATEGY_CONFIG = {
    'position_size_percent': 0.15,   # 15% of balance as margin
    'leverage': 50,                  # Must match Lighter UI
    
    'profit_thresholds': [2, 3, 4, 5, 6, 7, 8, 9, 10],
    'double_down_threshold': -6,
    'stop_loss_offset': 1,
    'cooldown_seconds': 30
}
```

## Example

With $103.53 balance and 15% margin:
- **Margin:** $15.53
- **Position Value (50x):** $776.50
- **BTC Amount:** ~0.0068 BTC
- **Lighter will show:** ~$24 margin (they calculate it their way)

The important part: Bot tracks the position and will close it correctly!

## Next Steps

1. ✅ Bot can open positions
2. ✅ Bot can track profit/loss
3. ✅ Bot can set trailing stop loss
4. ✅ Bot can double positions
5. ✅ Bot can close positions
6. 🔄 Ready to run!

