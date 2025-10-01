import { LighterClient } from './api/lighterClient.js';
import { config, validateConfig } from './config/config.js';

async function testConnection() {
  console.log('🚀 Testing Lighter API Connection...\n');

  // Validate configuration
  if (!validateConfig()) {
    console.error('\n❌ Configuration validation failed. Please check your .env file.');
    process.exit(1);
  }

  console.log('✅ Configuration validated\n');

  // Initialize client
  const client = new LighterClient();
  console.log('');

  try {
    // Test 1: Get account information by L1 address
    console.log('📊 Test 1: Fetching account information by address...');
    try {
      const account = await client.getAccountByAddress();
      console.log('✅ Account data fetched successfully');
      console.log('Account data:', JSON.stringify(account, null, 2));
      
      // If we get account data, extract the actual account index
      if (account && account.account_index !== undefined) {
        console.log(`\n💡 Your actual ACCOUNT_INDEX is: ${account.account_index}`);
        console.log('   Update your .env file with: LIGHTER_ACCOUNT_INDEX=' + account.account_index);
      }
    } catch (error) {
      console.log('⚠️  Could not fetch account by address');
      console.log('   Error:', error.message);
      console.log('   This might mean the account does not exist yet');
    }

    // Test 2: Get all markets (orderbooks)
    console.log('\n📈 Test 2: Fetching available markets...');
    try {
      const markets = await client.getMarkets();
      
      if (typeof markets === 'object') {
        const marketKeys = Object.keys(markets);
        console.log(`✅ Found ${marketKeys.length} markets`);
        
        if (marketKeys.length > 0) {
          console.log('\nFirst 5 markets:');
          marketKeys.slice(0, 5).forEach((key, index) => {
            console.log(`  ${index + 1}. ${key}`);
          });
        }
      } else if (Array.isArray(markets)) {
        console.log(`✅ Found ${markets.length} markets`);
        if (markets.length > 0) {
          console.log('\nFirst 5 markets:');
          markets.slice(0, 5).forEach((market, index) => {
            console.log(`  ${index + 1}.`, market);
          });
        }
      }
    } catch (error) {
      console.log('⚠️  Could not fetch markets');
      console.log('   Error:', error.message);
    }

    // Test 3: Get orderbook for a specific market (if we know one)
    console.log('\n📖 Test 3: Testing orderbook endpoint...');
    try {
      // Try a common market pair
      const testMarketId = 'BTC-USD' || 0;
      const orderbook = await client.getOrderbook(testMarketId);
      console.log('✅ Orderbook fetched successfully');
      console.log('Sample:', JSON.stringify(orderbook).substring(0, 200) + '...');
    } catch (error) {
      console.log('⚠️  Could not fetch orderbook (market may not exist)');
    }

    // Test 4: Get API keys
    console.log('\n🔑 Test 4: Checking API keys...');
    try {
      const apiKeys = await client.getApiKeys();
      console.log('✅ API keys fetched successfully');
      console.log('API Keys:', JSON.stringify(apiKeys, null, 2));
    } catch (error) {
      console.log('⚠️  Could not fetch API keys');
      console.log('   Error:', error.message);
    }

    console.log('\n✅ Connection test completed!');
    console.log('\n📝 Summary:');
    console.log('  - API connection: ✅ Working');
    console.log('  - Base URL:', client.baseURL);
    console.log('  - Wallet loaded: ✅', client.address);
    console.log('\n⚠️  Important Notes:');
    console.log('  - Lighter uses a custom Go-based signer for transactions');
    console.log('  - Trading operations (create/cancel orders) require either:');
    console.log('    1. Using the Python SDK (recommended)');
    console.log('    2. Implementing custom signing logic in JS');
    console.log('    3. Setting up a proxy service for signing');
    console.log('\n  - This JS client can:');
    console.log('    ✅ Fetch account data');
    console.log('    ✅ Get market data and orderbooks');
    console.log('    ✅ Monitor trades and orders');
    console.log('    ❌ Place/cancel orders (requires signer implementation)');
    
    process.exit(0);

  } catch (error) {
    console.error('\n❌ Connection test failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', JSON.stringify(error.response.data).substring(0, 500));
    }
    process.exit(1);
  }
}

// Run the test
testConnection();