import axios from 'axios';
import { ethers } from 'ethers';
import { config } from '../config/config.js';

export class LighterClient {
  constructor() {
    this.baseURL = config.api.baseURL;
    this.apiKeyPublic = config.api.apiKeyPublic;
    this.apiKeyPrivate = config.api.apiKeyPrivate;
    this.accountIndex = config.api.accountIndex;
    this.apiKeyIndex = config.api.apiKeyIndex;
    this.privateKey = config.blockchain.privateKey;
    
    // Initialize ethers wallet
    this.wallet = new ethers.Wallet(this.privateKey);
    this.address = this.wallet.address;
    
    // Create axios instance
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    console.log('📡 Lighter Client initialized');
    console.log(`   Base URL: ${this.baseURL}`);
    console.log(`   Wallet: ${this.address}`);
    console.log(`   Account Index: ${this.accountIndex}`);
    console.log(`   API Key Index: ${this.apiKeyIndex}`);
  }

  /**
   * Get account information by L1 address
   */
  async getAccountByAddress(address = null) {
    try {
      const addr = address || this.address;
      const path = `/api/account/by-l1-address/${addr}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get account:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get account information by index
   */
  async getAccountByIndex(accountIndex = null) {
    try {
      const index = accountIndex !== null ? accountIndex : this.accountIndex;
      const path = `/api/account/by-index/${index}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get account by index:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get all accounts by L1 address (master + subaccounts)
   */
  async getAllAccountsByAddress(address = null) {
    try {
      const addr = address || this.address;
      const path = `/api/account/accounts-by-l1-address/${addr}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get all accounts:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get API keys for an account
   */
  async getApiKeys(accountIndex = null, apiKeyIndex = 255) {
    try {
      const index = accountIndex !== null ? accountIndex : this.accountIndex;
      const path = `/api/account/apikeys/${index}/${apiKeyIndex}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get API keys:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get orderbook for a specific market
   */
  async getOrderbook(marketId) {
    try {
      const path = `/api/order/order-book-details/${marketId}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get orderbook:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get all orderbooks
   */
  async getAllOrderbooks() {
    try {
      const path = '/api/order/order-books';
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get orderbooks:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get markets list (using orderbooks endpoint)
   */
  async getMarkets() {
    try {
      const orderbooks = await this.getAllOrderbooks();
      return orderbooks;
    } catch (error) {
      console.error('Failed to get markets:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get next nonce for signing transactions
   */
  async getNextNonce(accountIndex = null, apiKeyIndex = null) {
    try {
      const accIdx = accountIndex !== null ? accountIndex : this.accountIndex;
      const keyIdx = apiKeyIndex !== null ? apiKeyIndex : this.apiKeyIndex;
      const path = `/api/transaction/next-nonce/${accIdx}/${keyIdx}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get next nonce:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get orders for an account
   */
  async getOrders(accountIndex = null) {
    try {
      const index = accountIndex !== null ? accountIndex : this.accountIndex;
      const path = `/api/order/orders/${index}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get orders:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Get trades for an account
   */
  async getTrades(accountIndex = null) {
    try {
      const index = accountIndex !== null ? accountIndex : this.accountIndex;
      const path = `/api/order/trades/${index}`;
      const response = await this.client.get(path);
      return response.data;
    } catch (error) {
      console.error('Failed to get trades:', error.response?.data || error.message);
      throw error;
    }
  }

  /**
   * Create auth token for websocket authentication
   * Note: In the Python SDK, this uses the signer binary
   * For JS, we'll need to implement the signing logic or use the API endpoint
   */
  async createAuthToken(expirySeconds = 3600) {
    try {
      // This would require implementing the custom signing logic
      // For now, returning a placeholder
      console.warn('⚠️  Auth token creation requires custom signing implementation');
      return null;
    } catch (error) {
      console.error('Failed to create auth token:', error.message);
      throw error;
    }
  }

  /**
   * Note: Order creation, modification, and cancellation require the Go signer binary
   * which is not easily portable to JavaScript. These would need either:
   * 1. A JS implementation of the signing logic
   * 2. A proxy service that handles signing
   * 3. Using the Python SDK instead
   */
  
  async placeOrder() {
    console.error('❌ Order placement requires the Go signer binary');
    console.error('   Consider using the Python SDK for trading operations');
    console.error('   Or implement custom signing logic based on lighter-go');
    throw new Error('Order placement not implemented in JS client');
  }
}