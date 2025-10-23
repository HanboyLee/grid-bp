"""
Strategy orchestration service
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    cancel_all_orders,
    create_orders,
    get_latest_strategy_state,
    list_orders,
    upsert_strategy_state,
)
from app.models.config import TradingConfig
from app.schemas.order import OrderCreate
from app.schemas.strategy import StrategyStartData, StrategyStopData, EmergencyCloseData
from app.services.backpack_client import BackpackClient
from app.services.grid_strategy import GridStrategy
from app.services.position_tracker import PositionTracker
from app.services.risk_manager import RiskManager

logger = logging.getLogger(__name__)


class StrategyService:
    """High level service coordinating strategy actions"""

    def __init__(self, db: AsyncSession, config: TradingConfig) -> None:
        self.db = db
        self.config = config
        self.grid_strategy = GridStrategy(config)
        self.position_tracker = PositionTracker()
        self.risk_manager = RiskManager(config, self.position_tracker)


    async def start(self, current_price: Optional[float] = None) -> StrategyStartData:
        """Start the strategy by calculating grids and placing buy orders"""
        state = await get_latest_strategy_state(self.db)
        if state and state.status == "RUNNING":
            logger.info("Strategy already running, returning existing state")
            grid_prices = [] if not self.grid_strategy.grid_prices else self.grid_strategy.grid_prices
            return StrategyStartData(
                status="RUNNING",
                start_time=state.start_time or datetime.now(timezone.utc),
                grid_prices=grid_prices,
                qty_per_grid=0.0,
            )

        if current_price is None:
            async with BackpackClient().session() as client:
                current_price = await client.get_symbol_price(self.config.symbol)
        current_price = current_price or 1.0

        grid_prices = self.grid_strategy.calculate_grid_prices(current_price)
        qty_per_grid = self.grid_strategy.calculate_quantity_per_grid(abs(grid_prices[0]) or current_price)

        # Create initial buy orders
        buy_levels = grid_prices[: len(grid_prices) // 2]
        orders = [
            OrderCreate(
                symbol=self.config.symbol,
                side="BUY",
                order_type="Limit",
                price=price,
                quantity=qty_per_grid,
                grid_level=index,
            )
            for index, price in enumerate(buy_levels)
        ]
        created_orders = await create_orders(self.db, orders)
        logger.info("Created %d initial buy orders", len(created_orders))

        now = datetime.now(timezone.utc)
        await upsert_strategy_state(
            self.db,
            {
                "status": "RUNNING",
                "start_time": now,
                "stop_time": None,
                "stop_reason": None,
                "total_capital": self.config.total_capital,
                "current_balance": self.config.total_capital,
                "total_realized_profit": 0.0,
                "total_unrealized_profit": 0.0,
                "grid_buy_orders": len(created_orders),
                "grid_sell_orders": 0,
                "current_grid_level": 0,
                "last_update": now,
            },
        )

        return StrategyStartData(
            status="RUNNING",
            start_time=now,
            grid_prices=grid_prices,
            qty_per_grid=qty_per_grid,
        )

    async def stop(self, reason: str = "MANUAL") -> StrategyStopData:
        """Stop strategy and cancel all orders"""
        cancelled = await cancel_all_orders(self.db)
        logger.info("Cancelled %d orders while stopping strategy", cancelled)

        now = datetime.now(timezone.utc)
        await upsert_strategy_state(
            self.db,
            {
                "status": "STOPPED",
                "stop_time": now,
                "stop_reason": reason,
                "last_update": now,
            },
        )

        return StrategyStopData(
            status="STOPPED",
            stop_time=now,
            stop_reason=reason,
        )

    async def emergency_close(self) -> EmergencyCloseData:
        """Emergency close cancels all orders and marks strategy as STOPPED"""
        pending_orders = await list_orders(self.db, limit=500)
        cancelled = await cancel_all_orders(self.db)
        await upsert_strategy_state(
            self.db,
            {
                "status": "STOPPED",
                "stop_time": datetime.now(timezone.utc),
                "stop_reason": "EMERGENCY_CLOSE",
            },
        )
        logger.warning("Emergency close executed, cancelled %d orders", cancelled)
        return EmergencyCloseData(
            closed_orders=len(pending_orders),
            message="Emergency close executed",
        )
