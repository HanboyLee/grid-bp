"""
Trading configuration model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base


class TradingConfig(Base):
    """Trading configuration table"""
    __tablename__ = "configs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    leverage = Column(Float, nullable=False)
    total_capital = Column(Float, nullable=False)
    grid_count = Column(Integer, nullable=False)
    price_range_percent = Column(Float, nullable=False)
    max_total_loss = Column(Float, nullable=False)
    target_profit = Column(Float, nullable=False)
    max_single_loss = Column(Float, nullable=True)
    status = Column(String(20), default="inactive")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    notes = Column(Text, nullable=True)
