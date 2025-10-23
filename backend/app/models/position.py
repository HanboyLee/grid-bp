"""
Position tracking model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Position(Base):
    """Positions table"""
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    size = Column(Float, nullable=False, default=0.0)
    average_price = Column(Float, nullable=False)
    side = Column(String(10), nullable=True)
    entry_time = Column(DateTime, nullable=True)
    current_price = Column(Float, nullable=True)
    unrealized_pnl = Column(Float, nullable=True)
    realized_pnl = Column(Float, nullable=True, default=0.0)
    margin_used = Column(Float, nullable=True)
    liquidation_price = Column(Float, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
