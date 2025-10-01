import WebSocket from 'ws';
import { config } from '../config/config.js';
import { EventEmitter } from 'events';

export class LighterWebSocket extends EventEmitter {
  constructor(lighterClient) {
    super();
    this.url = config.websocket.url;
    this.lighterClient = lighterClient;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 5000;
    this.subscriptions = new Set();
  }

  /**
   * Connect to WebSocket
   */
  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.on('open', () => {
          console.log('✅ WebSocket connected');
          this.reconnectAttempts = 0;
          this.resubscribeAll();
          resolve();
        });

        this.ws.on('message', (data) => {
          try {
            const message = JSON.parse(data.toString());
            this.handleMessage(message);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        });

        this.ws.on('error', (error) => {
          console.error('WebSocket error:', error.message);
          this.emit('error', error);
        });

        this.ws.on('close', () => {
          console.log('WebSocket disconnected');
          this.emit('close');
          this.handleReconnect();
        });

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Handle incoming WebSocket messages
   */
  handleMessage(message) {
    const { type, channel, data } = message;

    switch (type) {
      case 'orderbook':
        this.emit('orderbook', data);
        break;
      case 'trade':
        this.emit('trade', data);
        break;
      case 'order_update':
        this.emit('orderUpdate', data);
        break;
      case 'balance_update':
        this.emit('balanceUpdate', data);
        break;
      case 'ticker':
        this.emit('ticker', data);
        break;
      default:
        this.emit('message', message);
    }
  }

  /**
   * Subscribe to a channel
   */
  subscribe(channel, params = {}) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket not connected. Subscription will be queued.');
      this.subscriptions.add({ channel, params });
      return;
    }

    const subscription = {
      type: 'subscribe',
      channel,
      ...params,
    };

    this.ws.send(JSON.stringify(subscription));
    this.subscriptions.add({ channel, params });
    console.log(`📡 Subscribed to ${channel}`, params);
  }

  /**
   * Unsubscribe from a channel
   */
  unsubscribe(channel, params = {}) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return;
    }

    const unsubscription = {
      type: 'unsubscribe',
      channel,
      ...params,
    };

    this.ws.send(JSON.stringify(unsubscription));
    
    // Remove from subscriptions
    this.subscriptions = new Set(
      [...this.subscriptions].filter(
        sub => !(sub.channel === channel && JSON.stringify(sub.params) === JSON.stringify(params))
      )
    );
    
    console.log(`📡 Unsubscribed from ${channel}`, params);
  }

  /**
   * Resubscribe to all channels after reconnection
   */
  resubscribeAll() {
    this.subscriptions.forEach(({ channel, params }) => {
      this.subscribe(channel, params);
    });
  }

  /**
   * Handle reconnection logic
   */
  handleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    console.log(`🔄 Reconnecting... Attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);

    setTimeout(() => {
      this.connect().catch(error => {
        console.error('Reconnection failed:', error);
      });
    }, this.reconnectDelay);
  }

  /**
   * Disconnect WebSocket
   */
  disconnect() {
    if (this.ws) {
      this.reconnectAttempts = this.maxReconnectAttempts; // Prevent auto-reconnect
      this.ws.close();
      this.ws = null;
      console.log('WebSocket disconnected manually');
    }
  }

  /**
   * Check if WebSocket is connected
   */
  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
} 