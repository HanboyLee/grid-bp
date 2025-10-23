"""
API routes for the trading bot
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.config import ConfigCreate, ConfigRead
from app.schemas.order import OrderRead
from app.schemas.position import PositionRead
from app.schemas.response import ApiResponse
from app.schemas.strategy import StrategyStartRequest
from app.schemas.trade import TradeRead
from app.crud import (
    create_config,
    get_active_config,
    get_latest_strategy_state,
    list_orders,
    list_positions,
    list_trades,
)


router = APIRouter(prefix="/api")


@router.post("/config", response_model=ApiResponse)
async def save_config(
    config_data: ConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """Save trading configuration"""
    config = await create_config(db, config_data)
    return ApiResponse(
        code=0,
        message="配置保存成功",
        data=ConfigRead.model_validate(config).model_dump()
    )


@router.get("/config", response_model=ApiResponse)
async def get_config(db: AsyncSession = Depends(get_db)):
    """Get active trading configuration"""
    config = await get_active_config(db)
    if not config:
        return ApiResponse(code=404, message="未找到活跃配置", data=None)
    return ApiResponse(
        code=0,
        message="成功",
        data=ConfigRead.model_validate(config).model_dump()
    )


@router.post("/strategy/start", response_model=ApiResponse)
async def start_strategy(
    request: StrategyStartRequest | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Start trading strategy"""
    from app.services.strategy_service import StrategyService
    
    config = await get_active_config(db)
    if not config:
        return ApiResponse(code=400, message="请先配置交易参数", data=None)
    
    service = StrategyService(db, config)
    result = await service.start(current_price=request.current_price if request else None)
    
    return ApiResponse(
        code=0,
        message="策略已启动",
        data={
            "status": result.status,
            "start_time": result.start_time.isoformat(),
            "grid_prices": result.grid_prices,
            "qty_per_grid": result.qty_per_grid,
        }
    )


@router.post("/strategy/stop", response_model=ApiResponse)
async def stop_strategy(db: AsyncSession = Depends(get_db)):
    """Stop trading strategy"""
    from app.services.strategy_service import StrategyService
    
    config = await get_active_config(db)
    if not config:
        return ApiResponse(code=400, message="请先配置交易参数", data=None)
    
    service = StrategyService(db, config)
    result = await service.stop()
    
    return ApiResponse(
        code=0,
        message="策略已停止",
        data={
            "status": result.status,
            "stop_time": result.stop_time.isoformat(),
            "stop_reason": result.stop_reason,
        }
    )


@router.post("/strategy/emergency-close", response_model=ApiResponse)
async def emergency_close(db: AsyncSession = Depends(get_db)):
    """Emergency close all positions"""
    from app.services.strategy_service import StrategyService
    
    config = await get_active_config(db)
    if not config:
        return ApiResponse(code=400, message="请先配置交易参数", data=None)
    
    service = StrategyService(db, config)
    result = await service.emergency_close()
    
    return ApiResponse(
        code=0,
        message="紧急平仓已执行",
        data={
            "closed_orders": result.closed_orders,
            "message": result.message,
        }
    )


@router.get("/orders", response_model=ApiResponse)
async def get_orders(
    status: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get orders list"""
    orders = await list_orders(db, status, limit)
    return ApiResponse(
        code=0,
        message="成功",
        data=[OrderRead.model_validate(order).model_dump() for order in orders]
    )


@router.get("/positions", response_model=ApiResponse)
async def get_positions(db: AsyncSession = Depends(get_db)):
    """Get positions list"""
    positions = await list_positions(db)
    return ApiResponse(
        code=0,
        message="成功",
        data=[PositionRead.model_validate(pos).model_dump() for pos in positions]
    )


@router.get("/trades", response_model=ApiResponse)
async def get_trades(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Get trades history"""
    trades = await list_trades(db, limit)
    return ApiResponse(
        code=0,
        message="成功",
        data=[TradeRead.model_validate(trade).model_dump() for trade in trades]
    )


@router.get("/statistics", response_model=ApiResponse)
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Get trading statistics"""
    trades = await list_trades(db, limit=1000)
    positions = await list_positions(db)
    
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if (t.net_profit or 0) > 0)
    losing_trades = sum(1 for t in trades if (t.net_profit or 0) < 0)
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    total_profit = sum(t.net_profit or 0 for t in trades)
    
    return ApiResponse(
        code=0,
        message="成功",
        data={
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": round(win_rate, 2),
            "total_profit": round(total_profit, 2),
            "avg_profit_per_trade": round(total_profit / total_trades, 2) if total_trades > 0 else 0,
            "active_positions": len(positions),
        }
    )


@router.get("/status", response_model=ApiResponse)
async def get_status(db: AsyncSession = Depends(get_db)):
    """Get system status"""
    state = await get_latest_strategy_state(db)
    
    return ApiResponse(
        code=0,
        message="成功",
        data={
            "strategy_status": state.status if state else "STOPPED",
            "backpack_api_connected": False,
            "websocket_connected": False,
            "database_status": "OK",
            "start_time": state.start_time.isoformat() if state and state.start_time else None,
            "current_balance": state.current_balance if state else 0.0,
            "total_realized_profit": state.total_realized_profit if state else 0.0,
        }
    )
