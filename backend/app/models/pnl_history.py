"""
PnL history model
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class PnLHistory(Base):
    """PnL history table"""
    __tablename__ = "pnl_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    trade_date = Column(Date, nullable=False)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    total_profit = Column(Float, default=0.0)
    realized_profit = Column(Float, default=0.0)
    unrealized_profit = Column(Float, default=0.0)
    win_rate = Column(Float, default=0.0)
    avg_profit_per_trade = Column(Float, default=0.0)
    max_single_profit = Column(Float, default=0.0)
    max_single_loss = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
