import dotenv from 'dotenv';

dotenv.config();

export const config = {
  // API Configuration
  api: {
    baseURL: process.env.LIGHTER_API_URL || 'https://mainnet.zklighter.elliot.ai',
    apiKeyPublic: process.env.LIGHTER_API_KEY_PUBLIC,
    apiKeyPrivate: process.env.LIGHTER_API_KEY_PRIVATE,
    accountIndex: parseInt(process.env.LIGHTER_ACCOUNT_INDEX) || 0,
    apiKeyIndex: parseInt(process.env.LIGHTER_API_KEY_INDEX) || 2,
  },
  
  // Blockchain Configuration
  blockchain: {
    chainId: parseInt(process.env.CHAIN_ID) || 42161,
    rpcUrl: process.env.RPC_URL || 'https://arb1.arbitrum.io/rpc',
    privateKey: process.env.PRIVATE_KEY,
  },
  
  // WebSocket Configuration
  websocket: {
    url: process.env.LIGHTER_WS_URL || 'wss://ws.lighter.xyz',
  },
  
  // Trading Configuration
  trading: {
    enabled: process.env.TRADING_ENABLED === 'true',
    default: parseFloat(process.env.DEFAULT_SLIPPAGE) || 0.5,
    maxPositionSize: parseFloat(process.env.MAX_POSITION_SIZE) || 1000,
  },
};

// Validate required configuration
export function validateConfig() {
  const required = [
    { key: 'LIGHTER_API_KEY_PRIVATE', value: config.api.apiKeyPrivate },
    { key: 'PRIVATE_KEY', value: config.blockchain.privateKey },
  ];
  
  const missing = required.filter(item => !item.value);
  
  if (missing.length > 0) {
    console.error('❌ Missing required environment variables:');
    missing.forEach(item => console.error(`  - ${item.key}`));
    return false;
  }
  
  return true;
} 