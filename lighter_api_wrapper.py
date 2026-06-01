"""Minimal async REST wrapper around the public Lighter.xyz API.

Used by check_balance.py and check_positions.py to read account state without
pulling in the full signing SDK. Use as an async context manager:

    async with LighterAPIWrapper(base_url) as api:
        account = await api.get_account(account_index)
"""

import aiohttp


class LighterAPIWrapper:
    def __init__(self, base_url: str):
        self.base_url = (base_url or "").rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "LighterAPIWrapper":
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *exc) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def get_account(self, account_index: int) -> dict | None:
        """Fetch account state (balance, positions) by account index."""
        url = f"{self.base_url}/api/v1/account"
        params = {"by": "index", "value": account_index}
        try:
            async with self._session.get(url, params=params) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
        except Exception as e:  # noqa: BLE001 - surface network errors to caller
            print(f"⚠️ Error fetching account: {e}")
            return None
