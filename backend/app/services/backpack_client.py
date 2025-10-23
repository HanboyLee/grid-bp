"""
Backpack API client abstraction
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class BackpackClient:
    """Simple asynchronous client for Backpack API"""

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or settings.backpack_api_key
        self.secret_key = secret_key or settings.backpack_secret_key
        self.base_url = base_url or settings.backpack_api_url
        self._client: Optional[httpx.AsyncClient] = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator["BackpackClient"]:
        """Provide an async context manager for the client"""
        async with httpx.AsyncClient(base_url=self.base_url, timeout=5.0) as client:
            self._client = client
            try:
                yield self
            finally:
                self._client = None

    async def get_symbol_price(self, symbol: str) -> Optional[float]:
        """Fetch latest price for given symbol

        Note: This is a simplified implementation that falls back to mocked
        data when the remote API is unavailable.
        """
        if self._client is None:
            raise RuntimeError("BackpackClient session has not been initialized")

        endpoint = f"/api/v1/ticker?symbol={symbol}"
        try:
            response = await self._client.get(endpoint)
            response.raise_for_status()
            payload = response.json()
            price = payload.get("price") or payload.get("last")
            if price is not None:
                return float(price)
        except Exception as exc:  # pragma: no cover - network fallback
            logger.warning("Fallback to mocked price for %s: %s", symbol, exc)
        # Fallback to mocked price if API fails
        mocked_prices = {
            "SOL_USDC_PERP": 141.2,
            "BTC_USDC_PERP": 30000.0,
            "ETH_USDC_PERP": 2000.0,
        }
        return mocked_prices.get(symbol, 100.0)
