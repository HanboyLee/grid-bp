"""
Grid trading strategy implementation
"""
import logging

logger = logging.getLogger(__name__)


class GridStrategy:
    """Grid trading strategy manager"""

    def __init__(self, config):
        self.config = config
        self.grid_prices = []
        self.is_running = False

    def calculate_grid_prices(self, current_price: float) -> list[float]:
        """Calculate grid price levels based on current price and config"""
        range_percent = self.config.price_range_percent
        grid_count = self.config.grid_count

        range_amount = current_price * range_percent / 100
        bottom_price = current_price - range_amount
        top_price = current_price + range_amount
        step = (top_price - bottom_price) / (grid_count - 1)

        prices = [bottom_price + i * step for i in range(grid_count)]
        self.grid_prices = prices
        logger.info(
            "Generated %d grid levels from %.2f to %.2f",
            grid_count,
            bottom_price,
            top_price,
        )
        return prices

    def calculate_quantity_per_grid(self, base_price: float) -> float:
        """Calculate position size per grid level"""
        total_capital = self.config.total_capital
        grid_count = self.config.grid_count
        normalized_price = max(base_price, 0.01)
        qty_per_grid = total_capital / grid_count / normalized_price
        logger.info(
            "Calculated qty per grid: %.4f (total capital: %.2f, grids: %d)",
            qty_per_grid,
            total_capital,
            grid_count,
        )
        return qty_per_grid
