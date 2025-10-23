"""
Order management helpers
"""
from __future__ import annotations

import logging
from typing import Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreate
from app.crud.order import create_orders

logger = logging.getLogger(__name__)


class OrderManager:
    """Handles creation of grid orders"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_initial_buy_orders(
        self,
        symbol: str,
        prices: list[float],
        qty_per_grid: float,
    ) -> list:
        """Create the initial buy orders at lower grid levels"""
        buy_levels = prices[: len(prices) // 2]
        orders: list[OrderCreate] = []
        for idx, price in enumerate(buy_levels):
            orders.append(
                OrderCreate(
                    symbol=symbol,
                    side="BUY",
                    order_type="Limit",
                    price=price,
                    quantity=qty_per_grid,
                    grid_level=idx,
                )
            )
        created = await create_orders(self.db, orders)
        logger.info("Created %d initial buy orders", len(created))
        return created
