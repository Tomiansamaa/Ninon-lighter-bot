#!/usr/bin/env python3
"""Check what happened to our transaction hashes"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def check_tx():
    """Check transaction status"""
    
    base_url = os.getenv('LIGHTER_API_URL')
    
    # This is one of the tx_hashes from the terminal
    tx_hash = "8d72ff3d0f2d81eaa47e0ab8c43c28e390639b1486b8972023b54292d1c077019f83bc9a3ba1a3ba"
    
    print(f"Checking transaction: {tx_hash[:20]}...")
    print("=" * 70)
    
    async with aiohttp.ClientSession() as session:
        # Try different endpoints
        endpoints = [
            f"/api/v1/transaction/{tx_hash}",
            f"/api/v1/tx/{tx_hash}",
            f"/api/v1/transactions?tx_hash={tx_hash}",
        ]
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            print(f"\nTrying: {endpoint}")
            async with session.get(url) as resp:
                print(f"Status: {resp.status}")
                if resp.status == 200:
                    data = await resp.json()
                    print(f"Response: {data}")
                else:
                    text = await resp.text()
                    print(f"Error: {text[:200]}")

if __name__ == "__main__":
    asyncio.run(check_tx())

