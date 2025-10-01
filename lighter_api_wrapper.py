#!/usr/bin/env python3
"""
Lightweight wrapper for Lighter API - bypasses SDK validation issues
"""

import aiohttp
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class LighterAPIWrapper:
    """
    Direct HTTP wrapper for Lighter API data fetching
    Bypasses SDK validation issues
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def close(self):
        if self.session:
            await self.session.close()
    
    async def get_orderbook(self, market_id: int) -> Optional[Dict]:
        """Get orderbook for a specific market"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Note: market_id should be an integer
            url = f"{self.base_url}/api/v1/orderBookDetails?market_id={market_id}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    text = await response.text()
                    logger.error(f"Failed to get orderbook: HTTP {response.status}: {text[:200]}")
                    return None
        except Exception as e:
            logger.error(f"Error getting orderbook: {e}")
            return None
    
    async def get_account(self, account_index: int) -> Optional[Dict]:
        """Get account information"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            # Account API needs 'by' and 'value' parameters
            url = f"{self.base_url}/api/v1/account?by=index&value={account_index}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    text = await response.text()
                    logger.error(f"Failed to get account: HTTP {response.status}: {text[:200]}")
                    return None
        except Exception as e:
            logger.error(f"Error getting account: {e}")
            return None
    
    async def get_markets(self) -> Optional[Dict]:
        """Get list of available markets/orderbooks"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            url = f"{self.base_url}/api/v1/orderBooks"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    text = await response.text()
                    logger.error(f"Failed to get markets: HTTP {response.status}: {text[:200]}")
                    return None
        except Exception as e:
            logger.error(f"Error getting markets: {e}")
            return None
