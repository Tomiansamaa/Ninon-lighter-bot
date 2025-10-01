# 🚀 Lighter Bot - Quick Start

## ⚡ Quick Commands

```bash
# Run the trading bot
python3 lighter_bot.py

# Find your account index
python3 find_account_index.py

# Check credentials
cat .env

# Update SDK
pip3 install --upgrade lighter-sdk
```

## 🔑 Your Credentials

All configured in `.env`:
- ✅ API Keys: Set
- ✅ Wallet: 0xC843b738d7b34c97393e198E6dAA6c4Fb81bdB80
- ✅ Account #132577: Active

## 📊 Your Accounts

| Index | Type | Balance |
|-------|------|---------|
| 132577 | Standard | $0.01 |
| 281474976667491 | Premium | $103.81 |
| 281474976680495 | Premium | $1,091.26 |

**Current:** #132577

To switch accounts, edit `LIGHTER_ACCOUNT_INDEX` in `.env`

## 📖 Documentation

- **Full Guide**: `SUCCESS_SUMMARY.md`
- **Technical Details**: `LIGHTER_API_STATUS.md`
- **API Docs**: https://apidocs.lighter.xyz/docs

## 🎯 What's Working

✅ **Connection**: Verified and active
✅ **Authentication**: API keys validated
✅ **Account**: Found and loaded
✅ **SDK**: Installed and initialized

## 💻 Bot Features

Check `lighter_bot.py` for:
- Account information
- Market data
- Order management
- Trade history
- WebSocket support (coming)

## 🔧 Customize

Edit `lighter_bot.py` to add:
- Trading strategies
- Risk management
- Alerts and notifications
- Custom indicators

## ⚠️ Important

- Start with small amounts
- Test thoroughly before scaling
- Check Lighter SDK docs for exact API methods
- Keep your `.env` file secure

---

**Ready to trade!** 🚀
