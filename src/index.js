import { LighterClient } from './api/lighterClient.js';
import { LighterWebSocket } from './api/websocketClient.js';
import { config, validateConfig } from './config/config.js';

class TradingBot {
  constructor() {
    this.client = null;
    this.ws = null;
    this.isRunning = false;
    this.markets = [];
    this.positions = {};
  }

  /**
   * Initialize the trading bot
   */
  async initialize() {
    console.log('🤖 Initializing Lighter Trading Bot...\n');

    // Validate configuration
    if (!validateConfig()) {
      throw new Error('Configuration validation failed');
    }

    // Initialize API client
    this.client = new LighterClient();
    console.log(`✅ Connected with wallet: ${this.client.address}`);

    // Initialize WebSocket
    this.ws = new LighterWebSocket(this.client);
    this.setupWebSocketHandlers();

    // Load markets
    await this.loadMarkets();

    // Connect WebSocket
    await this.ws.connect();

    console.log('✅ Trading bot initialized successfully\n');
  }

  /**
   * Setup WebSocket event handlers
   */
  setupWebSocketHandlers() {
    this.ws.on('orderbook', (data) => {
      this.handleOrderbookUpdate(data);
    });

    this.ws.on('trade', (data) => {
      this.handleTradeUpdate(data);
    });

    this.ws.on('orderUpdate', (data) => {
      this.handleOrderUpdate(data);
    });

    this.ws.on('balanceUpdate', (data) => {
      this.handleBalanceUpdate(data);
    });

    this.ws.on('ticker', (data) => {
      this.handleTickerUpdate(data);
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.ws.on('close', () => {
      console.log('WebSocket connection closed');
    });
  }

  /**
   * Load available markets
   */
  async loadMarkets() {
    try {
      this.markets = await this.client.getMarkets();
      console.log(`📊 Loaded ${this.markets.length} markets`);
      
      if (this.markets.length > 0) {
        console.log('\nAvailable markets:');
        this.markets.forEach((market, index) => {
          console.log(`  ${index + 1}. ${market.symbol || market.id}`);
        });
      }
    } catch (error) {
      console.error('Failed to load markets:', error);
      throw error;
    }
  }

  /**
   * Handle orderbook updates
   */
  handleOrderbookUpdate(data) {
    console.log('📊 Orderbook update:', data);
    
    // Implement your trading strategy here
    // Example: Check for arbitrage opportunities, price levels, etc.
  }

  /**
   * Handle trade updates
   */
  handleTradeUpdate(data) {
    console.log('💱 Trade executed:', data);
  }

  /**
   * Handle order updates
   */
  handleOrderUpdate(data) {
    console.log('📝 Order update:', data);
  }

  /**
   * Handle balance updates
   */
  handleBalanceUpdate(data) {
    console.log('💰 Balance update:', data);
  }

  /**
   * Handle ticker updates
   */
  handleTickerUpdate(data) {
    console.log('📈 Ticker update:', data);
  }

  /**
   * Subscribe to market data
   */
  async subscribeToMarket(marketId) {
    if (!this.ws.isConnected()) {
      console.warn('WebSocket not connected');
      return;
    }

    this.ws.subscribe('orderbook', { market: marketId });
    this.ws.subscribe('trades', { market: marketId });
    this.ws.subscribe('ticker', { market: marketId });
    
    console.log(`📡 Subscribed to market: ${marketId}`);
  }

  /**
   * Place a market order
   */
  async placeMarketOrder(marketId, side, size) {
    if (!config.trading.enabled) {
      console.warn('⚠️  Trading is disabled. Set TRADING_ENABLED=true in .env to enable.');
      return null;
    }

    try {
      const order = await this.client.placeOrder({
        market: marketId,
        side: side, // 'buy' or 'sell'
        type: 'market',
        size: size,
      });

      console.log(`✅ Market order placed: ${side} ${size} on ${marketId}`);
      return order;
    } catch (error) {
      console.error('Failed to place order:', error);
      throw error;
    }
  }

  /**
   * Place a limit order
   */
  async placeLimitOrder(marketId, side, size, price) {
    if (!config.trading.enabled) {
      console.warn('⚠️  Trading is disabled. Set TRADING_ENABLED=true in .env to enable.');
      return null;
    }

    try {
      const order = await this.client.placeOrder({
        market: marketId,
        side: side, // 'buy' or 'sell'
        type: 'limit',
        size: size,
        price: price,
      });

      console.log(`✅ Limit order placed: ${side} ${size} @ ${price} on ${marketId}`);
      return order;
    } catch (error) {
      console.error('Failed to place order:', error);
      throw error;
    }
  }

  /**
   * Get current balances
   */
  async getBalances() {
    try {
      const balances = await this.client.getBalances();
      console.log('💰 Current balances:', balances);
      return balances;
    } catch (error) {
      console.error('Failed to get balances:', error);
      throw error;
    }
  }

  /**
   * Get active orders
   */
  async getActiveOrders(marketId = null) {
    try {
      const orders = await this.client.getActiveOrders(marketId);
      console.log('📝 Active orders:', orders);
      return orders;
    } catch (error) {
      console.error('Failed to get active orders:', error);
      throw error;
    }
  }

  /**
   * Start the trading bot
   */
  async start() {
    if (this.isRunning) {
      console.warn('Trading bot is already running');
      return;
    }

    this.isRunning = true;
    console.log('\n🚀 Trading bot started!\n');

    // Subscribe to markets
    if (this.markets.length > 0) {
      // Subscribe to the first market as an example
      await this.subscribeToMarket(this.markets[0].id);
    }

    // Example: Get balances periodically
    setInterval(async () => {
      try {
        await this.getBalances();
      } catch (error) {
        console.error('Error getting balances:', error);
      }
    }, 60000); // Every minute

    // Keep the bot running
    console.log('Bot is now monitoring markets...');
    console.log('Press Ctrl+C to stop\n');
  }

  /**
   * Stop the trading bot
   */
  async stop() {
    console.log('\n🛑 Stopping trading bot...');
    this.isRunning = false;
    
    if (this.ws) {
      this.ws.disconnect();
    }

    console.log('✅ Trading bot stopped');
    process.exit(0);
  }
}

// Main execution
async function main() {
  const bot = new TradingBot();

  try {
    await bot.initialize();
    await bot.start();

    // Handle graceful shutdown
    process.on('SIGINT', async () => {
      await bot.stop();
    });

    process.on('SIGTERM', async () => {
      await bot.stop();
    });

  } catch (error) {
    console.error('❌ Bot initialization failed:', error);
    process.exit(1);
  }
}

// Run the bot
main(); 