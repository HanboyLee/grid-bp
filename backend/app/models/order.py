"""
Order model definitions
"""
from uuid import uuid4
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Order(Base):
    """Orders table"""
    __tablename__ = "orders"
    
    id = Column(String(100), primary_key=True, default=lambda: str(uuid4()))
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)
    order_type = Column(String(20), nullable=False, default="Limit")
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    executed_quantity = Column(Float, nullable=True, default=0.0)
    status = Column(String(20), nullable=False, default="PENDING")
    grid_level = Column(Integer, nullable=True)
    paired_order_id = Column(String(100), ForeignKey("orders.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    filled_at = Column(DateTime, nullable=True)
    average_fill_price = Column(Float, nullable=True)
    commission = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    paired_order = relationship("Order", remote_side=[id])
