"""
Risk management helpers
"""
from __future__ import annotations

import logging
from typing import Protocol
from app.services.position_tracker import PositionTracker

logger = logging.getLogger(__name__)


class SupportsRiskConfig(Protocol):
    """Protocol describing config attributes used by risk manager"""

    total_capital: float
    price_range_percent: float
    max_total_loss: float
    target_profit: float


class RiskManager:
    """Performs basic risk checks"""

    def __init__(self, config: SupportsRiskConfig, position_tracker: PositionTracker):
        self.config = config
        self.position_tracker = position_tracker

    def calculate_leverage_ratio(self) -> float:
        """Calculate leverage ratio based on current positions"""
        total_capital = self.config.total_capital
        if total_capital == 0:
            return 0.0
        margin_used = self.position_tracker.total_size * self.config.price_range_percent / 100
        leverage_ratio = margin_used / total_capital
        logger.debug(
            "Leverage ratio calculated: %.4f (margin_used=%.2f, total_capital=%.2f)",
            leverage_ratio,
            margin_used,
            total_capital,
        )
        return leverage_ratio

    def check_global_stop_loss(self, total_loss: float) -> bool:
        """Check if total loss exceeds configured limit"""
        exceeded = total_loss <= -abs(self.config.max_total_loss)
        if exceeded:
            logger.warning("Global stop loss triggered: %.2f", total_loss)
        return exceeded

    def check_global_take_profit(self, total_profit: float) -> bool:
        """Check if total profit reaches target"""
        reached = total_profit >= self.config.target_profit
        if reached:
            logger.info("Global take profit triggered: %.2f", total_profit)
        return reached
