"""
Pydantic schemas for strategy operations
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StrategyStartRequest(BaseModel):
    current_price: Optional[float] = Field(default=None, description="最新市场价格")


class StrategyStartData(BaseModel):
    status: str
    start_time: datetime
    grid_prices: list[float]
    qty_per_grid: float


class StrategyStopData(BaseModel):
    status: str
    stop_time: datetime
    stop_reason: str


class EmergencyCloseData(BaseModel):
    closed_orders: int
    message: str
