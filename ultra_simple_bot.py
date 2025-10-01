#!/usr/bin/env python3
"""
SIMPLEST BOT - No calculations, just BTC amount
"""
import os
import asyncio
import lighter
import time
import aiohttp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('LIGHTER_API_URL')
API_KEY_PRIVATE = os.getenv('LIGHTER_API_KEY_PRIVATE')
ACCOUNT_INDEX = int(os.getenv('LIGHTER_ACCOUNT_INDEX'))
API_KEY_INDEX = int(os.getenv('LIGHTER_API_KEY_INDEX', '10'))

# SIMPLE SETTINGS - Percentage-based
BTC_AMOUNT = 0.0000025  # Change this to trade more/less BTC
TARGET_PROFIT_PERCENT = 1.0  # Close at +1% profit (price drops 1% for SHORT)
FIRST_DOUBLE_LOSS_USD = -0.3  # First doubling at -$0.25
SECOND_DOUBLE_LOSS_USD = -2  # Second doubling (triple) at -$1.50


async def get_price():
    """Get BTC price"""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/api/v1/orderBookDetails?market_id=1"
        async with session.get(url) as response:
            data = await response.json()
            return float(data['order_book_details'][0]['last_trade_price'])


async def get_live_position():
    """Get actual live position from Lighter"""
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/api/v1/account?by=index&value={ACCOUNT_INDEX}"
        async with session.get(url) as response:
            data = await response.json()
            
            # Check for positions
            account = data.get('account') or (data.get('accounts', [{}])[0] if data.get('accounts') else {})
            positions = account.get('positions', [])
            
            # Find BTC position
            for pos in positions:
                if pos.get('symbol') == 'BTC' or pos.get('market_id') == 1:
                    position_btc = float(pos.get('position', 0)) / 1e8  # Convert from satoshis
                    entry_price = float(pos.get('avg_entry_price', 0))
                    unrealized_pnl = float(pos.get('unrealized_pnl', 0))
                    
                    if position_btc != 0:
                        return {
                            'size': abs(position_btc),
                            'entry_price': entry_price,
                            'pnl_usd': unrealized_pnl,
                            'is_short': position_btc < 0
                        }
            
            return None


async def place_take_profit_percent(client, entry_price, position_size_btc, profit_percent):
    """Place TP order based on percentage POSITION profit (accounting for leverage)"""
    
    # For SHORT with 50x leverage:
    # 1% position profit = 1% / 50 = 0.02% price movement
    leverage = 50
    price_movement_percent = profit_percent / leverage
    
    # For SHORT: profit when price DROPS
    target_price_float = entry_price * (1 - price_movement_percent / 100)
    
    # For Lighter limit orders, multiply by 10
    take_profit_price = int(target_price_float * 10)
    
    print(f"\n🎯 TAKE PROFIT Order ({profit_percent}% position profit):")
    print(f"   Entry Price: ${entry_price:,.2f}")
    print(f"   Position Size: {position_size_btc:.8f} BTC")
    print(f"   Leverage: {leverage}x")
    print(f"   Target: {profit_percent}% position profit = {price_movement_percent:.3f}% price drop")
    print(f"   TP Price: ${target_price_float:,.2f}")
    
    tp_client_order_index = int(time.time() * 1000) % 2147483647
    base_amount = int(position_size_btc * 1e8)
    
    try:
        tp_order_result, tp_tx_hash, tp_order_id = await client.create_order(
            market_index=1,
            client_order_index=tp_client_order_index,
            base_amount=base_amount,
            price=take_profit_price,
            is_ask=False,  # BUY to close SHORT
            order_type=5,  # ORDER_TYPE_TAKE_PROFIT
            time_in_force=1,  # GOOD_TILL_TIME
            reduce_only=True,
            trigger_price=take_profit_price
        )
        print(f"✅ TP order placed: {tp_tx_hash}")
        return tp_client_order_index
    except Exception as e:
        print(f"⚠️ TP order failed: {e}")
        return None


async def open_short(client):
    """Open SHORT - just send BTC amount, no calculations"""
    price = await get_price()
    base_amount = int(BTC_AMOUNT * 1e8)  # Convert to satoshis
    
    print(f"\n🔴 OPENING SHORT")
    print(f"BTC: {BTC_AMOUNT} BTC")
    print(f"Price: ${price:,.2f}")
    
    client_order_index = int(time.time() * 1000) % 2147483647
    order_result, tx_hash, order_id = await client.create_market_order(
        market_index=1,
        client_order_index=client_order_index,
        base_amount=base_amount,
        avg_execution_price=int(price),
        is_ask=True,  # SHORT = SELL
        reduce_only=False
    )
    
    print(f"✅ SHORT opened: {tx_hash}")
    return price
    


async def close_short(client):
    """Close SHORT"""
    price = await get_price()
    base_amount = int(BTC_AMOUNT * 1e8)
    
    print(f"\n🟢 CLOSING SHORT")
    print(f"Price: ${price:,.2f}")
    
    client_order_index = int(time.time() * 1000) % 2147483647
    order_result, tx_hash, order_id = await client.create_market_order(
        market_index=1,
        client_order_index=client_order_index,
        base_amount=base_amount,
        avg_execution_price=int(price),
        is_ask=False,  # BUY to close SHORT
        reduce_only=False
    )
    
    print(f"✅ Closed: {tx_hash}")


async def main():
    print("🤖 SIMPLEST BOT - PERCENTAGE-BASED")
    print(f"Amount: {BTC_AMOUNT} BTC")
    print(f"Take Profit: {TARGET_PROFIT_PERCENT}% position profit")
    print(f"First double at: ${FIRST_DOUBLE_LOSS_USD}")
    print(f"Second double (triple) at: ${SECOND_DOUBLE_LOSS_USD}")
    print(f"Will automatically open new position after each TP\n")
    
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX
    )
    
    try:
        while True:  # Infinite loop
            # Open new position
            entry_price = await open_short(client)
            
            # Wait 1 second for position to register
            await asyncio.sleep(1)
            position = await get_live_position()
            if position and position['size'] > 0.000001:
                print(f"✅ Position confirmed: {position['size']:.8f} BTC at ${position['entry_price']:.2f}")
            
            if position and position['size'] > 0.000001:
                tp_order_index = await place_take_profit_percent(
                    client, 
                    position['entry_price'], 
                    position['size'], 
                    TARGET_PROFIT_PERCENT
                )
            else:
                print("⚠️ Could not get position after 10 seconds - using entry price")
                tp_order_index = await place_take_profit_percent(
                    client, 
                    entry_price, 
                    BTC_AMOUNT, 
                    TARGET_PROFIT_PERCENT
                )
            
            first_doubled = False
            second_doubled = False
            
            print(f"\n📊 Monitoring for TP or doubling...")
            
            # Monitor until position closes (TP hit) or needs doubling
            position_active = True
            while position_active:
                await asyncio.sleep(2)
                
                position = await get_live_position()
                
                if not position:
                    print("✅ Position closed (TP hit)! Waiting 3 seconds before new position...")
                    await asyncio.sleep(3)
                    break  # Exit inner loop to open new position
            
                current_price = await get_price()
                pnl_usd = position['pnl_usd']
                
                # Calculate P&L percentage for SHORT
                pnl_percent = ((position['entry_price'] - current_price) / position['entry_price']) * 100
                
                emoji = "🟢" if pnl_usd >= 0 else "🔴"
                print(f"{emoji} P&L: ${pnl_usd:+.2f} ({pnl_percent:+.2f}%) | Entry: ${position['entry_price']:,.2f} | Now: ${current_price:,.2f}")
                
                # Position will close automatically via TP order at {TARGET_PROFIT_PERCENT}%
                
                # Check for second doubling (triple position)
                if pnl_usd <= SECOND_DOUBLE_LOSS_USD and first_doubled and not second_doubled:
                    print(f"\n⚠️⚠️ MAJOR LOSS at ${pnl_usd:.2f} → TRIPLING POSITION (2nd double)")
                    try:
                        # Cancel old TP
                        if tp_order_index:
                            try:
                                await client.create_cancel_order(1, tp_order_index)
                                print("✅ Old TP cancelled")
                            except:
                                pass
                        
                        # Add another position
                        await open_short(client)
                        await asyncio.sleep(2)
                        
                        # Get new position and place new TP
                        new_position = await get_live_position()
                        if new_position:
                            tp_order_index = await place_take_profit_percent(
                                client,
                                new_position['entry_price'],
                                new_position['size'],
                                TARGET_PROFIT_PERCENT
                            )
                        
                        second_doubled = True
                        print(f"✅ Position tripled! New TP set for {TARGET_PROFIT_PERCENT}%\n")
                    except Exception as e:
                        print(f"❌ Failed to triple: {e}\n")
                
                # Check for first doubling
                elif pnl_usd <= FIRST_DOUBLE_LOSS_USD and not first_doubled:
                    print(f"\n⚠️ Loss at ${pnl_usd:.2f} → DOUBLING POSITION")
                    try:
                        # Cancel old TP
                        if tp_order_index:
                            try:
                                await client.create_cancel_order(1, tp_order_index)
                                print("✅ Old TP cancelled")
                            except:
                                pass
                        
                        # Double position
                        await open_short(client)
                        await asyncio.sleep(2)
                        
                        # Get new position and place new TP
                        new_position = await get_live_position()
                        if new_position:
                            tp_order_index = await place_take_profit_percent(
                                client,
                                new_position['entry_price'],
                                new_position['size'],
                                TARGET_PROFIT_PERCENT
                            )
                        
                        first_doubled = True
                        print(f"✅ Position doubled! New TP set for {TARGET_PROFIT_PERCENT}%\n")
                    except Exception as e:
                        print(f"❌ Failed to double: {e}\n")
                
    except KeyboardInterrupt:
        print("\n\n⚠️ Bot stopped by user")
        print("Note: Take profit orders remain active in Lighter")
        print("Check Lighter UI to manage any open positions")


if __name__ == "__main__":
    asyncio.run(main())
