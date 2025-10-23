"""
Pydantic schemas for trades
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TradeRead(BaseModel):
    id: int
    symbol: str
    buy_order_id: Optional[str]
    sell_order_id: Optional[str]
    buy_price: float
    sell_price: float
    quantity: float
    profit_per_unit: Optional[float]
    total_profit: Optional[float]
    fee: Optional[float]
    net_profit: Optional[float]
    pnl_percent: Optional[float]
    entry_time: Optional[datetime]
    exit_time: Optional[datetime]
    hold_duration: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True
