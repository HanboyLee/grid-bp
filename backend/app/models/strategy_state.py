"""
Strategy state tracking model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class StrategyState(Base):
    """Strategy state table"""
    __tablename__ = "strategy_state"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(20), nullable=True)
    start_time = Column(DateTime, nullable=True)
    stop_time = Column(DateTime, nullable=True)
    stop_reason = Column(String(50), nullable=True)
    total_capital = Column(Float, nullable=True)
    current_balance = Column(Float, nullable=True)
    total_realized_profit = Column(Float, nullable=True)
    total_unrealized_profit = Column(Float, nullable=True)
    grid_buy_orders = Column(Integer, nullable=True)
    grid_sell_orders = Column(Integer, nullable=True)
    current_grid_level = Column(Integer, nullable=True)
    last_update = Column(DateTime, server_default=func.now(), onupdate=func.now())
