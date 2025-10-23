"""
CRUD helpers for trades
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.trade import Trade


async def list_trades(db: AsyncSession, limit: int = 50):
    """Return all trades"""
    result = await db.execute(
        select(Trade).order_by(Trade.exit_time.desc()).limit(limit)
    )
    return result.scalars().all()
