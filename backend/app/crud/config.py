"""
CRUD operations for TradingConfig
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.config import TradingConfig
from app.schemas.config import ConfigCreate


async def create_config(db: AsyncSession, config_data: ConfigCreate) -> TradingConfig:
    """Create a new trading configuration"""
    # Deactivate existing configs first
    await deactivate_configs(db)
    
    db_config = TradingConfig(**config_data.model_dump())
    db.add(db_config)
    await db.flush()
    await db.refresh(db_config)
    return db_config


async def get_active_config(db: AsyncSession) -> TradingConfig | None:
    """Get the currently active trading configuration"""
    result = await db.execute(
        select(TradingConfig).where(TradingConfig.status == "active").order_by(TradingConfig.id.desc())
    )
    return result.scalars().first()


async def deactivate_configs(db: AsyncSession):
    """Deactivate all existing configs"""
    await db.execute(
        update(TradingConfig).where(TradingConfig.status == "active").values(status="inactive")
    )
    await db.flush()
