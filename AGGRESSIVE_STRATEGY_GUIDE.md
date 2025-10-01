# ⚡ Aggressive 50x Leverage Strategy Guide

## 🎯 Your Custom Strategy

This bot implements YOUR exact strategy:

### Strategy Details:

1. **Position Opening:**
   - Use 5% of balance
   - Apply 50x leverage
   - Choose LONG or SHORT

2. **Trailing Stop Loss:**
   ```
   Profit → Stop Loss
   +2%   → -1%  (locks in +1%)
   +3%   → -2%  (locks in +2%)
   +4%   → -3%  (locks in +3%)
   +5%   → -4%  (locks in +4%)
   ... and so on
   ```

3. **Martingale (Doubling):**
   - If position reaches -6%
   - Double the position size
   - Average down the entry price
   - ⚠️ Very risky!

4. **After Stop Loss:**
   - Wait 60 seconds (cooldown)
   - Open new position

---

## ⚠️ EXTREME RISK WARNING

### Why This Strategy Is EXTREMELY RISKY:

**50x Leverage:**
- A 2% move against you = 100% position loss
- A 1% move = 50% gain or loss
- Can be liquidated in seconds
- Total account loss possible

**Martingale (Doubling):**
- Can turn small losses into huge losses
- Example: -6% becomes -12% if doubled position also loses
- Can drain entire account quickly
- Famous for blowing up accounts

**Math Example:**
```
Starting Balance: $1,000
Position: 5% = $50
With 50x leverage = $2,500 exposure

Scenario 1 - Win:
+2% move = +$50 profit (100% gain on position!)

Scenario 2 - Loss:
-2% move = -$50 loss (100% position loss)
-4% move = -$100 loss (MORE than position!)

With Doubling:
First position: -6% = -$150
Double position: -6% = -$300
Total loss: -$450 (45% of account!)
```

---

## 🚀 How to Use

### Step 1: Test in Paper Mode FIRST!

```bash
# Make sure paper mode is ON
nano aggressive_bot_config.py

# Check this line:
TRADING_ENABLED = False  # Must be False for testing!
```

### Step 2: Run Paper Trading

```bash
python3 run_aggressive_bot.py
```

This will simulate trades without real money.

### Step 3: Watch the Logs

```bash
# In another terminal
tail -f aggressive_bot.log
```

You'll see:
- Position openings
- Profit updates every 5 seconds
- Trailing stop adjustments
- Double downs (if triggered)
- Stop loss triggers

### Step 4: Let It Run for Days

**Test for at least 7 days** in paper mode:
- Monitor different market conditions
- Watch how often stop loss triggers
- See how many times it doubles down
- Calculate total P&L

### Step 5: Go Live (When Ready)

⚠️ **ONLY IF YOU'RE READY TO LOSE IT ALL!**

```python
# In aggressive_bot_config.py
TRADING_ENABLED = True
```

**Start with TINY amounts!**

---

## ⚙️ Configuration

### Basic Settings

Edit `aggressive_bot_config.py`:

```python
# Position size (5% default)
'position_size_percent': 0.05,

# Leverage (50x default)
'leverage': 50,

# Double down threshold (-6% default)
'double_down_threshold': -6,

# Cooldown after stop loss (60s default)
'cooldown_seconds': 60,
```

### Conservative Adjustments

For **slightly** less risk (still very risky!):

```python
# Smaller positions
'position_size_percent': 0.02,  # 2% instead of 5%

# Lower leverage
'leverage': 20,  # 20x instead of 50x

# More conservative double down
'double_down_threshold': -10,  # -10% instead of -6%
```

### Aggressive Adjustments

For **even more** risk (not recommended!):

```python
# Larger positions
'position_size_percent': 0.10,  # 10% instead of 5%

# Higher leverage
'leverage': 100,  # 100x (!!!)

# Earlier double down
'double_down_threshold': -4,  # -4% instead of -6%
```

---

## 📊 Understanding Performance

### Monitoring Your Bot:

```bash
# Watch real-time
tail -f aggressive_bot.log

# Search for key events
grep "STOP LOSS" aggressive_bot.log
grep "DOUBLING" aggressive_bot.log
grep "Position opened" aggressive_bot.log
```

### Key Metrics to Track:

1. **Win Rate**
   - How often does stop loss trigger with profit vs loss?

2. **Average Profit**
   - What's the average P&L per trade?

3. **Max Drawdown**
   - Worst losing streak

4. **Double Down Frequency**
   - How often does it double?
   - How often does doubling save you?
   - How often does it make losses worse?

5. **Time in Position**
   - Average time before stop loss?

---

## 🎓 Expected Behaviors

### Normal Operation:

```
1. Bot opens position (LONG or SHORT)
2. Monitors every 5 seconds
3. Updates trailing stop as profit increases
4. Either:
   a) Hits stop loss (win or small loss)
   b) Reaches -6% and doubles
   c) After doubling, hits stop loss
5. Enters 60s cooldown
6. Opens new position
7. Repeat
```

### What You'll See:

```
📤 OPENING NEW POSITION
💰 Balance: $1000.00
📊 Current Price: $50000.00
📈 Position Size: 0.001 (5% of balance)
⚡ Leverage: 50x
🟢 LONG

🟢 Position P&L: +0.8% | Entry: $50000 | Current: $50200 | Stop: None
🟢 Position P&L: +1.2% | Entry: $50000 | Current: $50300 | Stop: None
🟢 Position P&L: +2.4% | Entry: $50000 | Current: $50600 | Stop: +1%
📈 Trailing stop updated: None → +1%
🟢 Position P&L: +3.1% | Entry: $50000 | Current: $50775 | Stop: +1%
📈 Trailing stop updated: +1% → +2%
🔴 Position P&L: +1.8% | Entry: $50000 | Current: $50450 | Stop: +2%

🛑 STOP LOSS TRIGGERED!
📊 Entry Price: $50000
💰 Exit Price: $50450
📉 Final P&L: +1.8%
```

---

## 🛡️ Safety Recommendations

### Must-Have Safety Measures:

1. **Start Paper Trading**
   - Test for minimum 1 week
   - Understand all scenarios

2. **Use Tiny Amounts**
   - Start with $100 or less
   - Something you can afford to lose completely

3. **Set Stop Loss on Account Level**
   - If account drops 20%, stop bot
   - Manual intervention

4. **Monitor Constantly**
   - Especially first 24 hours
   - Be ready to stop immediately

5. **Have Exit Plan**
   - Know when to stop (losses)
   - Know when to stop (profits)
   - Stick to the plan!

6. **Don't Get Greedy**
   - If it works, don't increase position size quickly
   - Scale very gradually
   - Take profits

### Red Flags to Stop Immediately:

- ❌ Multiple double downs in a row
- ❌ Account down more than 20%
- ❌ Bot behaving unexpectedly
- ❌ Extreme market volatility
- ❌ You're stressed/worried
- ❌ Any technical issues

---

## 📝 Files You Have

```
run_aggressive_bot.py              - Main bot
aggressive_leverage_strategy.py    - Strategy logic
aggressive_bot_config.py           - Configuration
AGGRESSIVE_STRATEGY_GUIDE.md       - This file
aggressive_bot.log                 - Log file (created when running)
```

---

## 🔧 Troubleshooting

### Bot Won't Start

```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip3 install --upgrade lighter-sdk

# Verify credentials
cat .env
```

### Positions Not Opening

1. Check if in cooldown period
2. Verify balance is sufficient
3. Check market is active
4. Review logs for errors

### Too Many Losses

1. **STOP THE BOT**
2. Review strategy parameters
3. Check market conditions
4. Consider if strategy suits current market
5. Reduce position size or leverage

---

## 📈 Example Scenarios

### Best Case Scenario:

```
Entry: $50,000
Position hits +10% → Stop at +9%
With 50x leverage: 9% × 50 = 450% profit on position!
On $50 position = $225 profit
```

### Worst Case Scenario:

```
Entry: $50,000
Position hits -6% → Doubles position
Doubled position hits -6% more
Total loss: ~$300 on $1,000 account (30%!)
```

### Realistic Scenario:

```
10 trades:
- 6 winners: Average +2% = +600%
- 4 losers: Average -3% = -600%
Net: Break even or small profit/loss
BUT: High stress, high risk of big loss
```

---

## 🎯 Success Tips

1. **Understand Completely**
   - Know how every part works
   - Test all scenarios in paper mode

2. **Start Microscopic**
   - Use smallest possible amounts
   - Scale up VERY slowly

3. **Stay Disciplined**
   - Don't override the bot manually
   - Stick to your stop loss rules
   - Take profits

4. **Monitor Markets**
   - Best in moderately volatile markets
   - Avoid during major news
   - Watch for unusual conditions

5. **Keep Learning**
   - Track what works
   - Adjust parameters gradually
   - Learn from losses

---

## ⚠️ Final Warning

This strategy has:
- ✅ High profit potential
- ❌ VERY high risk
- ❌ High stress
- ❌ Can lose everything quickly

**Only use if:**
- You fully understand the risks
- You can afford to lose 100%
- You can handle the stress
- You can monitor constantly
- You're experienced with trading

**Most professional traders would NOT use this strategy!**

---

## 🚀 Ready to Start?

```bash
# 1. Review configuration
cat aggressive_bot_config.py

# 2. Make sure paper mode is ON
nano aggressive_bot_config.py

# 3. Run the bot
python3 run_aggressive_bot.py

# 4. Monitor logs
tail -f aggressive_bot.log
```

**Test for at least 7 days before considering live trading!**

---

**Good luck, trade safely, and never risk more than you can afford to lose!** 📈⚡💰

*Remember: Most aggressive strategies blow up eventually. Have a plan to stop.*
