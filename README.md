# Lighter BTC Short Bot

A small **Python** trading bot for [Lighter.xyz](https://lighter.xyz) (a perpetuals
DEX on Arbitrum). It opens leveraged **short** positions on BTC, sets a take-profit
target that adapts to recent volatility, and uses a martingale-style ladder that
scales the position up if the trade moves against it.

> ⚠️ **High-risk strategy — read this first.** This bot uses **50x leverage** and a
> **martingale doubling** ladder (1x → 2x → 4x → 8x on a losing position). Martingale
> can wipe out an account during a sustained move. This code is shared for
> **educational purposes only**. It is not financial advice. Never run it with funds
> you cannot afford to lose, and test with the smallest possible size first.

## What it does

- Connects to Lighter via the official `lighter` Python SDK (`SignerClient`)
- Polls the BTC orderbook and tracks recent prices to estimate volatility (standard deviation)
- Opens a market **short** on BTC and places a reduce-only **take-profit** order
- Recomputes the take-profit target as volatility changes and re-places the order
- Adds to the position at preset loss thresholds (martingale ladder)
- Loops: after a take-profit fills, it opens a fresh position

## Repository layout

| File | Purpose |
|------|---------|
| `ultra_simple_bot.py` | Main bot — volatility-adaptive take-profit + martingale short strategy |
| `find_account_index.py` | Helper — derives your L1 address from your key and looks up your Lighter account index |
| `check_balance.py` | Helper — prints your available USDC balance |
| `check_positions.py` | Helper — prints open positions and recent orders |
| `lighter_api_wrapper.py` | Minimal async REST wrapper used by the helper scripts |

## Prerequisites

- Python 3.10+
- A funded [Lighter.xyz](https://lighter.xyz) account on Arbitrum
- Lighter API key credentials

## Installation

```bash
# 1. Create a virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install the Lighter SDK (not on PyPI)
pip install git+https://github.com/elliottech/lighter-python.git
```

## Configuration

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `LIGHTER_API_URL` | Lighter API endpoint (e.g. `https://mainnet.zklighter.elliot.ai`) |
| `PRIVATE_KEY` | Your Ethereum wallet private key (used locally to derive your L1 address) |
| `LIGHTER_API_KEY_PRIVATE` | Lighter API key private key, used to sign orders |
| `LIGHTER_ACCOUNT_INDEX` | Your Lighter account index (see below) |
| `LIGHTER_API_KEY_INDEX` | Lighter API key index (default `10`) |

⚠️ **Never commit your `.env` or share your keys.** `.env` is already gitignored.

## Usage

```bash
# Find your account index (writes nothing — just prints it)
python find_account_index.py

# Sanity-check your account before trading
python check_balance.py
python check_positions.py

# Run the bot
python ultra_simple_bot.py
```

Stop the bot with `Ctrl+C`. Note that any take-profit orders it placed remain
active on Lighter — manage open positions from the Lighter UI.

## Strategy parameters

Tunable constants at the top of `ultra_simple_bot.py`:

- `BTC_AMOUNT` — base position size in BTC (default `0.000015`)
- `FIRST_DOUBLE_LOSS_USD` / `SECOND_DOUBLE_LOSS_USD` / `THIRD_DOUBLE_LOSS_USD` — USD loss
  thresholds that trigger the 2x / 4x / 8x martingale steps

Take-profit adapts to volatility (standard deviation of recent % price changes):

| Volatility (STD) | Take-profit target |
|------------------|--------------------|
| < 0.03% | 1.2% |
| 0.03–0.08% | 1.8% |
| 0.08–0.15% | 2.5% |
| 0.15–0.25% | 3.5% |
| > 0.25% | 5.0% |

## Resources

- [Lighter API docs](https://apidocs.lighter.xyz/docs)
- [Lighter Python SDK](https://github.com/elliottech/lighter-python)

## Disclaimer

This software is provided for educational purposes only and carries significant
financial risk. Trading leveraged crypto perpetuals can result in the total loss of
your funds. Do your own research and never trade more than you can afford to lose.

## License

[MIT](LICENSE) © 2025 Tomi Ansamaa
