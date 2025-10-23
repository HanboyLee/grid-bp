"""
CRUD operations for StrategyState
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.strategy_state import StrategyState


async def get_latest_strategy_state(db: AsyncSession) -> StrategyState | None:
    """Get the latest strategy state"""
    result = await db.execute(
        select(StrategyState).order_by(StrategyState.id.desc())
    )
    return result.scalars().first()


async def upsert_strategy_state(db: AsyncSession, state_data: dict) -> StrategyState:
    """Create or update strategy state"""
    existing = await get_latest_strategy_state(db)
    
    if existing:
        for key, value in state_data.items():
            setattr(existing, key, value)
        await db.flush()
        await db.refresh(existing)
        return existing
    else:
        new_state = StrategyState(**state_data)
        db.add(new_state)
        await db.flush()
        await db.refresh(new_state)
        return new_state
