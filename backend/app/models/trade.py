"""
Trade history model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base


class Trade(Base):
    """Trades table"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    buy_order_id = Column(String(100), nullable=True)
    sell_order_id = Column(String(100), nullable=True)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    profit_per_unit = Column(Float, nullable=True)
    total_profit = Column(Float, nullable=True)
    fee = Column(Float, nullable=True)
    net_profit = Column(Float, nullable=True)
    pnl_percent = Column(Float, nullable=True)
    entry_time = Column(DateTime, nullable=True)
    exit_time = Column(DateTime, nullable=True)
    hold_duration = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
