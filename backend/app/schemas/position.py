"""
Pydantic schemas for positions
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PositionRead(BaseModel):
    id: int
    symbol: str
    size: float
    average_price: float
    side: Optional[str]
    entry_time: Optional[datetime]
    current_price: Optional[float]
    unrealized_pnl: Optional[float]
    realized_pnl: Optional[float]
    margin_used: Optional[float]
    liquidation_price: Optional[float]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
