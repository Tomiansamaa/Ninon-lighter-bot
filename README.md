# Lighter Trading Bot

A JavaScript/Node.js trading bot for [Lighter.xyz](https://lighter.xyz) - a decentralized spot order book exchange on Arbitrum.

## 📋 Features

- ✅ REST API integration with Lighter.xyz
- ✅ WebSocket support for real-time market data
- ✅ EIP-712 signature authentication
- ✅ Market and limit order execution
- ✅ Real-time orderbook monitoring
- ✅ Balance and position tracking
- ✅ Configurable trading strategies
- ✅ Error handling and auto-reconnection

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- A wallet with some funds on Arbitrum network
- Lighter.xyz API credentials (obtained through their platform)

### Installation

1. **Clone or navigate to the project directory:**

```bash
cd LighterKoodi
```

2. **Install dependencies:**

```bash
npm install
```

3. **Configure environment variables:**

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
# Lighter API Configuration
LIGHTER_API_URL=https://api.lighter.xyz
LIGHTER_API_KEY=your_api_key_here
LIGHTER_API_SECRET=your_api_secret_here
LIGHTER_API_PASSPHRASE=your_passphrase_here

# Blockchain Configuration (Arbitrum)
CHAIN_ID=42161
RPC_URL=https://arb1.arbitrum.io/rpc
PRIVATE_KEY=your_private_key_here

# WebSocket Configuration
LIGHTER_WS_URL=wss://ws.lighter.xyz

# Trading Configuration
TRADING_ENABLED=false
DEFAULT_SLIPPAGE=0.5
MAX_POSITION_SIZE=1000
```

⚠️ **Security Warning:** Never commit your `.env` file or share your private keys!

## 📚 API Credentials Setup

### Getting Your API Key

To use the Lighter API, you need to:

1. Visit [Lighter.xyz](https://lighter.xyz) and connect your wallet
2. Navigate to the API section in your account settings
3. Generate API credentials (API Key, Secret, and Passphrase)
4. Add these credentials to your `.env` file

Alternatively, you can create API credentials programmatically using the bot:

```javascript
import { LighterClient } from './src/api/lighterClient.js';

const client = new LighterClient();
const credentials = await client.createApiKey();
console.log('API Credentials:', credentials);
```

## 🧪 Testing Connection

Before running the bot, test your connection:

```bash
npm run test
```

This will:
- Validate your configuration
- Test REST API connectivity
- Fetch available markets
- Test WebSocket connection
- Display your account information

## 🎯 Usage

### Running the Bot

Start the trading bot:

```bash
npm start
```

For development with auto-reload:

```bash
npm run dev
```

### Basic Trading Examples

#### 1. Place a Market Order

```javascript
await bot.placeMarketOrder('WETH-USDC', 'buy', 0.1);
```

#### 2. Place a Limit Order

```javascript
await bot.placeLimitOrder('WETH-USDC', 'buy', 0.1, 1800);
```

#### 3. Get Account Balances

```javascript
const balances = await bot.getBalances();
```

#### 4. Get Active Orders

```javascript
const orders = await bot.getActiveOrders();
```

#### 5. Subscribe to Market Data

```javascript
await bot.subscribeToMarket('WETH-USDC');
```

## 🏗️ Project Structure

```
LighterKoodi/
├── src/
│   ├── api/
│   │   ├── lighterClient.js      # REST API client
│   │   └── websocketClient.js    # WebSocket client
│   ├── config/
│   │   └── config.js             # Configuration management
│   ├── index.js                  # Main bot entry point
│   └── test-connection.js        # Connection test script
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
├── package.json                  # Node.js dependencies
└── README.md                     # This file
```

## 🔐 Authentication

Lighter uses a two-level authentication system:

### L1: Private Key Authentication
- Used for critical operations like creating API keys
- Signs EIP-712 typed data with your wallet
- Never exposed to the server

### L2: API Key Authentication
- Used for trading operations
- HMAC-SHA256 signatures
- Includes API key, secret, and passphrase

## 📊 Trading Configuration

Configure trading parameters in `.env`:

- `TRADING_ENABLED`: Enable/disable actual trading (default: `false`)
- `DEFAULT_SLIPPAGE`: Maximum acceptable slippage (default: `0.5%`)
- `MAX_POSITION_SIZE`: Maximum position size (default: `1000`)

## 🛡️ Security Best Practices

1. **Never share your private key or API credentials**
2. **Use environment variables** for sensitive data
3. **Start with TRADING_ENABLED=false** to test
4. **Use small amounts** when testing live
5. **Monitor your positions** regularly
6. **Keep your dependencies updated**
7. **Review the code** before running

## 📡 WebSocket Events

The bot listens to various WebSocket events:

- `orderbook` - Orderbook updates
- `trade` - Trade executions
- `orderUpdate` - Your order status changes
- `balanceUpdate` - Account balance changes
- `ticker` - Price ticker updates

## 🐛 Troubleshooting

### "Configuration validation failed"
- Check that all required environment variables are set in `.env`
- Verify your API credentials are correct

### "WebSocket connection failed"
- Check your internet connection
- Verify the WebSocket URL is correct
- Check if Lighter.xyz services are operational

### "Failed to place order"
- Ensure `TRADING_ENABLED=true` in `.env`
- Verify you have sufficient balance
- Check order parameters (size, price, etc.)

## 📖 Resources

- [Lighter API Documentation](https://apidocs.lighter.xyz/docs)
- [Lighter Documentation](https://docs.lighter.xyz)
- [Lighter Website](https://lighter.xyz)
- [Arbitrum Network](https://arbitrum.io)

## ⚖️ Disclaimer

This software is for educational purposes only. Trading cryptocurrencies carries significant risk. Always:

- Test thoroughly before live trading
- Start with small amounts
- Never invest more than you can afford to lose
- Do your own research
- Understand the risks involved

## 📄 License

MIT License - feel free to use and modify as needed.

## 🤝 Support

For issues or questions:
- Check the [Lighter documentation](https://docs.lighter.xyz)
- Visit Lighter's Discord or Telegram channels
- Review the API documentation at [apidocs.lighter.xyz](https://apidocs.lighter.xyz/docs)

---

**Happy Trading! 🚀** 