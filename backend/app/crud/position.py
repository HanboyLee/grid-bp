"""
CRUD helpers for positions
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.position import Position


async def list_positions(db: AsyncSession):
    """Return all positions"""
    result = await db.execute(select(Position).order_by(Position.updated_at.desc()))
    return result.scalars().all()
