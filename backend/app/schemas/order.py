"""
Pydantic schemas for orders
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    symbol: str
    side: str = Field(description="BUY or SELL")
    order_type: str = Field(default="Limit", description="订单类型")
    price: float = Field(gt=0)
    quantity: float = Field(gt=0)
    grid_level: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: str
    executed_quantity: Optional[float] = 0.0
    status: str
    paired_order_id: Optional[str] = None
    created_at: datetime
    filled_at: Optional[datetime] = None
    average_fill_price: Optional[float] = None
    commission: Optional[float] = None
    pnl: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
