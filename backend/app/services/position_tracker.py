"""
Position tracking service
"""
import logging

logger = logging.getLogger(__name__)


class PositionTracker:
    """Tracks open positions and P&L"""

    def __init__(self):
        self.total_size = 0.0
        self.total_realized_profit = 0.0
        self.total_realized_loss = 0.0

    def update_position(self, quantity: float, side: str) -> None:
        """Update position size based on new order"""
        if side.upper() == "BUY":
            self.total_size += quantity
            logger.debug("Position increased by %.4f", quantity)
        elif side.upper() == "SELL":
            self.total_size -= quantity
            logger.debug("Position decreased by %.4f", quantity)

    def record_pnl(self, pnl: float) -> None:
        """Record realized PnL from closed trade"""
        if pnl > 0:
            self.total_realized_profit += pnl
        else:
            self.total_realized_loss += abs(pnl)
        logger.info("Recorded PnL: %.2f", pnl)
