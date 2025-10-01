#!/usr/bin/env python3
"""
Simple Trading Bot - Based on test_short_order.py that WORKED
Adds trailing stop loss and position doubling logic
"""
import os
import asyncio
import lighter
import time
from dotenv import load_dotenv
from lighter_api_wrapper import LighterAPIWrapper

# Load environment
load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL', 'https://mainnet.zklighter.elliot.ai')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', '10'))

# Strategy settings
POSITION_MARGIN_PERCENT = 0.05  # 5% of balance as margin
LEVERAGE = 50  # 50x leverage
PROFIT_THRESHOLD = 2  # Set stop loss when profit reaches 2%
STOP_LOSS_OFFSET = 1  # Stop loss 1% behind profit
DOUBLE_DOWN_THRESHOLD = -6  # Double position at -6% loss
CHECK_INTERVAL = 5  # Check every 5 seconds

# Position tracking
current_position = None
entry_price = None
position_size_btc = None
highest_profit = 0
current_stop_loss = None
has_doubled = False


async def get_current_btc_price():
    """Get current BTC price from Lighter API"""
    wrapper = LighterAPIWrapper(BASE_URL)
    orderbook = await wrapper.get_orderbook(1)  # market_id=1 for BTC
    await wrapper.close()
    
    if orderbook and 'order_book_details' in orderbook:
        btc_data = orderbook['order_book_details'][0]
        return float(btc_data['last_trade_price'])
    return None


async def get_account_balance():
    """Get available balance"""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            url = f"{BASE_URL}/api/v1/account?by=index&value={ACCOUNT_INDEX}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Check both possible formats
                    if data and 'accounts' in data and data['accounts']:
                        balance = float(data['accounts'][0].get('available_balance', 0))
                        print(f"💰 Fetched balance: ${balance:.2f}")
                        return balance
                    elif data and 'account' in data:
                        balance = float(data['account'].get('available_balance', 0))
                        print(f"💰 Fetched balance: ${balance:.2f}")
                        return balance
        print("⚠️ Could not get account data")
        return 0
    except Exception as e:
        print(f"❌ Balance fetch error: {e}")
        import traceback
        traceback.print_exc()
        return 0


async def open_long_position(client, balance):
    """Open a LONG position - Modified for LONG trades"""
    global current_position, entry_price, position_size_btc, highest_profit, current_stop_loss, has_doubled
    
    print("\n" + "=" * 70)
    print("📤 OPENING LONG POSITION")
    print("=" * 70)
    
    # Get current price
    current_price = await get_current_btc_price()
    if not current_price:
        print("❌ Cannot get price")
        return False
    
    # Calculate position - EXACT formula from test_short_order.py
    margin = balance * POSITION_MARGIN_PERCENT
    total_position_value = margin * LEVERAGE
    position_size_btc = total_position_value / current_price
    base_amount = int(position_size_btc * 1e8)
    
    # Get best ask for LONG (buying)
    wrapper = LighterAPIWrapper(BASE_URL)
    orderbook = await wrapper.get_orderbook(1)
    await wrapper.close()
    
    if orderbook and 'order_book_details' in orderbook:
        btc_data = orderbook['order_book_details'][0]
        best_ask = float(btc_data.get('best_ask_price', current_price))
    else:
        best_ask = current_price
    
    avg_execution_price = int(best_ask)
    client_order_index = int(time.time() * 1000) % 2147483647
    
    print(f"💰 Balance: ${balance:.2f}")
    print(f"💵 Margin: ${margin:.2f} ({POSITION_MARGIN_PERCENT*100}% of balance)")
    print(f"⚡ Leverage: {LEVERAGE}x")
    print(f"📈 Position Value: ${total_position_value:.2f}")
    print(f"📊 Position Size: {position_size_btc:.8f} BTC = {base_amount} sats")
    print(f"💲 Entry Price: ${current_price:,.2f}")
    print(f"🎯 Execution Price: ${avg_execution_price:,}")
    
    try:
        # Place LONG order (BUY)
        order_result, tx_hash, order_id = await client.create_market_order(
            market_index=1,  # BTC
            client_order_index=client_order_index,
            base_amount=base_amount,
            avg_execution_price=avg_execution_price,
            is_ask=False,  # LONG = BUY
            reduce_only=False
        )
        
        print(f"✅ Order submitted! TX: {tx_hash}")
        
        # Initialize tracking
        current_position = True
        entry_price = current_price
        highest_profit = 0
        current_stop_loss = None
        has_doubled = False
        
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


async def close_position(client):
    """Close the current LONG position"""
    global current_position, entry_price, position_size_btc
    
    print("\n" + "=" * 70)
    print("🔴 CLOSING POSITION")
    print("=" * 70)
    
    current_price = await get_current_btc_price()
    if not current_price:
        print("❌ Cannot get price")
        return False
    
    # Calculate P&L for LONG (profit when price goes up)
    pnl_percent = ((current_price - entry_price) / entry_price) * 100
    print(f"📊 Entry: ${entry_price:,.2f}")
    print(f"📊 Exit: ${current_price:,.2f}")
    print(f"💰 P&L: {pnl_percent:+.2f}%")
    
    # Close by placing opposite (SHORT/SELL) order
    base_amount = int(position_size_btc * 1e8)
    
    wrapper = LighterAPIWrapper(BASE_URL)
    orderbook = await wrapper.get_orderbook(1)
    await wrapper.close()
    
    if orderbook and 'order_book_details' in orderbook:
        btc_data = orderbook['order_book_details'][0]
        best_bid = float(btc_data.get('best_bid_price', current_price))
    else:
        best_bid = current_price
    
    avg_execution_price = int(best_bid)
    client_order_index = int(time.time() * 1000) % 2147483647
    
    try:
        # Place SHORT (SELL) order to close LONG
        order_result, tx_hash, order_id = await client.create_market_order(
            market_index=1,
            client_order_index=client_order_index,
            base_amount=base_amount,
            avg_execution_price=avg_execution_price,
            is_ask=True,  # SHORT = SELL (to close LONG)
            reduce_only=False
        )
        
        print(f"✅ Position closed! TX: {tx_hash}")
        print("=" * 70)
        
        # Reset tracking
        current_position = None
        entry_price = None
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to close: {e}")
        return False


async def monitor_position(client):
    """Monitor position and apply trading logic"""
    global highest_profit, current_stop_loss, has_doubled, position_size_btc
    
    current_price = await get_current_btc_price()
    if not current_price:
        return
    
    # Calculate P&L (LONG: profit when price goes up)
    pnl_percent = ((current_price - entry_price) / entry_price) * 100
    
    # Update highest profit
    if pnl_percent > highest_profit:
        highest_profit = pnl_percent
    
    # Set/update trailing stop loss
    if pnl_percent >= PROFIT_THRESHOLD and current_stop_loss is None:
        current_stop_loss = PROFIT_THRESHOLD - STOP_LOSS_OFFSET
        print(f"🎯 Profit reached {pnl_percent:.2f}% → Stop loss set at {current_stop_loss:.2f}%")
    elif pnl_percent > PROFIT_THRESHOLD:
        new_stop = pnl_percent - STOP_LOSS_OFFSET
        if new_stop > current_stop_loss:
            current_stop_loss = new_stop
            print(f"📈 Stop loss moved to {current_stop_loss:.2f}% (trailing)")
    
    # Display status
    stop_str = f"{current_stop_loss:.2f}%" if current_stop_loss else "None"
    emoji = "🟢" if pnl_percent >= 0 else "🔴"
    print(f"{emoji} P&L: {pnl_percent:+.2f}% | Entry: ${entry_price:,.2f} | Current: ${current_price:,.2f} | SL: {stop_str}")
    
    # Check stop loss
    if current_stop_loss and pnl_percent <= current_stop_loss:
        print(f"🛑 Stop loss triggered at {pnl_percent:.2f}%!")
        await close_position(client)
        return
    
    # Check double down
    if pnl_percent <= DOUBLE_DOWN_THRESHOLD and not has_doubled:
        print(f"⚠️ Loss reached {pnl_percent:.2f}% → DOUBLING POSITION")
        balance = await get_account_balance()
        if balance > 0:
            # Double the position size
            margin = balance * POSITION_MARGIN_PERCENT
            total_position_value = margin * LEVERAGE * 2  # DOUBLE
            new_position_size = total_position_value / current_price
            position_size_btc += new_position_size
            has_doubled = True
            print(f"✅ Position doubled! New size: {position_size_btc:.8f} BTC")


async def main():
    """Main trading loop"""
    print("\n" + "=" * 70)
    print("🤖 SIMPLE TRADING BOT - BASED ON WORKING TEST CODE")
    print("=" * 70)
    print(f"Account: {ACCOUNT_INDEX}")
    print(f"Margin: {POSITION_MARGIN_PERCENT*100}%")
    print(f"Leverage: {LEVERAGE}x")
    print(f"Profit Threshold: {PROFIT_THRESHOLD}%")
    print(f"Double Down: {DOUBLE_DOWN_THRESHOLD}%")
    print("=" * 70)
    
    # Initialize client
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    print("✅ Client initialized\n")
    
    try:
        while True:
            if not current_position:
                # No position - open one
                balance = await get_account_balance()
                if balance > 0:
                    await open_long_position(client, balance)
                    await asyncio.sleep(CHECK_INTERVAL)
                else:
                    print("❌ Insufficient balance")
                    break
            else:
                # Monitor existing position
                await monitor_position(client)
                await asyncio.sleep(CHECK_INTERVAL)
                
    except KeyboardInterrupt:
        print("\n\n👋 Stopping bot...")
        if current_position:
            print("Closing open position...")
            await close_position(client)


if __name__ == "__main__":
    asyncio.run(main())
