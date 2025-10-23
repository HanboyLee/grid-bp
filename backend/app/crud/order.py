"""
CRUD operations for Orders
"""
from collections.abc import Iterable
from typing import Sequence
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.schemas.order import OrderCreate


async def create_orders(db: AsyncSession, orders: Iterable[OrderCreate]) -> Sequence[Order]:
    """Create multiple orders"""
    created_orders: list[Order] = []
    for order in orders:
        db_order = Order(**order.model_dump())
        db.add(db_order)
        created_orders.append(db_order)
    await db.flush()
    for order in created_orders:
        await db.refresh(order)
    return created_orders


async def list_orders(db: AsyncSession, status: str | None = None, limit: int = 50) -> Sequence[Order]:
    """List orders optionally filtered by status"""
    stmt = select(Order).order_by(Order.created_at.desc()).limit(limit)
    if status:
        stmt = stmt.where(Order.status == status.upper())
    result = await db.execute(stmt)
    return result.scalars().all()


async def cancel_orders_by_status(db: AsyncSession, status: str) -> int:
    """Cancel orders matching a specific status"""
    result = await db.execute(
        update(Order)
        .where(Order.status == status.upper())
        .values(status="CANCELLED")
    )
    await db.flush()
    return result.rowcount or 0


async def cancel_all_orders(db: AsyncSession) -> int:
    """Cancel all pending orders"""
    result = await db.execute(
        update(Order)
        .values(status="CANCELLED")
    )
    await db.flush()
    return result.rowcount or 0
