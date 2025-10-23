"""
Pydantic schemas for trading configuration
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ConfigBase(BaseModel):
    symbol: str = Field(description="交易对,例如 SOL_USDC_PERP")
    leverage: float = Field(gt=0, description="杠杆倍数")
    total_capital: float = Field(gt=0, description="总资金")
    grid_count: int = Field(ge=2, description="网格数量")
    price_range_percent: float = Field(gt=0, description="价格区间百分比")
    max_total_loss: float = Field(description="最大总亏损")
    target_profit: float = Field(description="目标利润")
    max_single_loss: Optional[float] = Field(default=None, description="单个网格最大亏损")
    notes: Optional[str] = None


class ConfigCreate(ConfigBase):
    status: str = Field(default="active", description="配置状态")


class ConfigRead(ConfigBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
