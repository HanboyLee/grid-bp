# Backpack 期货网格交易机器人 - 完整项目文档

**项目名称**：Grid Trading Bot for Backpack Exchange  
**创建日期**：2025年10月23日  
**版本**：v1.0  
**作者**：Team Dev

---

## 📋 目录

1. [项目概述](#项目概述)
2. [技术栈](#技术栈)
3. [系统架构](#系统架构)
4. [功能需求](#功能需求)
5. [数据库设计](#数据库设计)
6. [API 设计](#api-设计)
7. [前端设计](#前端设计)
8. [后端逻辑](#后端逻辑)
9. [风险管理](#风险管理)
10. [部署方案](#部署方案)
11. [开发计划](#开发计划)

---

## 项目概述

### 1.1 项目目标

实现一个自动化的期货网格交易机器人,用户可以通过 Web 界面配置交易参数,系统自动在 Backpack 交易所执行网格交易策略,并实时展示订单状态和收益情况。

### 1.2 核心功能

- ✅ **用户参数配置**:通过 Web UI 设置交易对、杠杆、资金、网格数等
- ✅ **自动网格生成**:根据当前价格和参数自动计算网格价位
- ✅ **自动交易执行**:分批建仓、动态平仓、自动重仓
- ✅ **全局止盈/止损**:达到目标利润或亏损额时自动停止
- ✅ **订单管理**:展示已委托、已成交、待平仓等所有订单
- ✅ **实时数据推送**:WebSocket 实时推送价格、订单更新
- ✅ **性能统计**:总收益、胜率、收益率等
- ✅ **风险管理**:爆仓保护、单个网格最大损失限制

### 1.3 使用场景

用户在 Backpack 交易所有 500 USDC,想在 SOL_USDC_PERP 上执行网格交易:

```
用户输入参数:
- 交易对:SOL_USDC_PERP
- 资金:500 USDC
- 杠杆:2x
- 网格数:10
- 价格区间:±10%(相对当前价格)
- 全局止损:-100 USDC
- 全局止盈:+300 USDC

系统自动:
1. 查询当前 SOL 价格(假设 141.2 USDC)
2. 计算价格范围:127.08 ~ 155.32 USDC
3. 生成 10 个网格价位
4. 在底部分批建仓
5. 监听价格变化
6. 价格上升时平仓获利
7. 价格下降时继续建仓
8. 达到止盈或止损时停止并清仓
```

---

## 技术栈

### 2.1 后端技术栈

| 组件 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **框架** | Python FastAPI | 0.104+ | RESTful API、WebSocket 服务 |
| **异步处理** | AsyncIO | 内置 | 异步事件循环、并发处理 |
| **数据库** | SQLite + SQLAlchemy | 3.13+ | 订单、配置、历史数据存储 |
| **WebSocket** | Python WebSocket | 12.0+ | 实时数据推送 |
| **HTTP 客户端** | httpx/aiohttp | 0.25+ | 调用 Backpack API |
| **日志** | Python logging | 内置 | 日志记录和调试 |
| **配置管理** | Pydantic | 2.0+ | 环境变量和配置验证 |
| **加密** | cryptography | 41.0+ | ED25519 签名认证 |

**Python 版本**:3.10+

**依赖包列表**(requirements.txt):
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
aiosqlite==0.19.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
websockets==12.0
python-dotenv==1.0.0
cryptography==41.0.7
```

### 2.2 前端技术栈

| 组件 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **框架** | Next.js | 14.0+ | 全栈框架 + React UI |
| **语言** | TypeScript | 5.0+ | 类型安全的 JavaScript |
| **UI 组件库** | shadcn/ui | 最新 | 美观的组件 |
| **样式** | Tailwind CSS | 3.0+ | Utility-first CSS 框架 |
| **状态管理** | Zustand | 4.4+ | 轻量级全局状态管理 |
| **HTTP 客户端** | fetch API / axios | 内置 | 调用后端 API |
| **图表库** | recharts | 2.10+ | 订单历史和收益图表 |
| **表格** | TanStack Table | 8.0+ | 高性能订单表格 |
| **实时通信** | WebSocket | 内置 | 连接后端 WebSocket |
| **表单验证** | React Hook Form + Zod | 最新 | 表单处理和验证 |

**Node 版本**:18.17+

### 2.3 部署环境

| 服务 | 技术 | 用途 |
|------|------|------|
| **容器化** | Docker | 应用打包和隔离 |
| **编排** | Docker Compose | 多容器编排 |
| **应用服务器** | Uvicorn (Python) | 后端 ASGI 服务器 |
| **应用服务器** | Node.js (Next.js) | 前端应用服务器 |
| **反向代理** | Nginx | 可选,生产环境负载均衡 |

---

## 系统架构

### 3.1 整体架构图

```
┌──────────────────────────────────────────────────────────────────┐
│                         Backpack Exchange                        │
│                      (REST API + WebSocket)                      │
└────────────────────────────────────────────────────────────────┬─┘
                              ▲
                              │ HTTP + WebSocket
                              │
                ┌─────────────┴──────────────────┐
                │                                │
    ┌───────────▼────────────────┐   ┌─────────▼──────────────────┐
    │   Python FastAPI 后端      │   │   Next.js 前端              │
    │  (:8000)                   │   │  (:3000)                    │
    │                            │   │                             │
    │ ┌──────────────────────┐   │   │ ┌─────────────────────────┐ │
    │ │ API Endpoints        │   │   │ │ Pages                   │ │
    │ ├──────────────────────┤   │   │ ├─────────────────────────┤ │
    │ │ /api/config          │◄──┼───┤ │ /dashboard              │ │
    │ │ /api/orders          │◄──┼───┤ │ /config                 │ │
    │ │ /api/positions       │◄──┼───┤ │ /orders                 │ │
    │ │ /api/strategy/start  │◄──┼───┤ │ /statistics             │ │
    │ │ /api/strategy/stop   │◄──┼───┤ │                         │ │
    │ │ /api/status          │◄──┼───┤ │ ┌─────────────────────┐ │ │
    │ │ /ws (WebSocket)      │◄──┼───┤ │ │ Components          │ │ │
    │ └──────────────────────┘   │   │ │ ├─────────────────────┤ │ │
    │                            │   │ │ │ ConfigForm          │ │ │
    │ ┌──────────────────────┐   │   │ │ │ OrderTable          │ │ │
    │ │ Core Services        │   │   │ │ │ Dashboard           │ │ │
    │ ├──────────────────────┤   │   │ │ │ StatsCard           │ │ │
    │ │ GridStrategy         │   │   │ │ │ WebSocketClient     │ │ │
    │ │ OrderManager         │   │   │ │ └─────────────────────┘ │ │
    │ │ PositionTracker      │   │   │ └─────────────────────────┘ │
    │ │ RiskManager          │   │   │                             │
    │ └──────────────────────┘   │   │ ┌─────────────────────────┐ │
    │                            │   │ │ State Management        │ │
    │ ┌──────────────────────┐   │   │ ├─────────────────────────┤ │
    │ │ Backpack Integration │   │   │ │ Zustand Store           │ │
    │ ├──────────────────────┤   │   │ │ - strategy state        │ │
    │ │ BackpackClient       │   │   │ │ - orders                │ │
    │ │ WebSocket Manager    │   │   │ │ - config                │ │
    │ └──────────────────────┘   │   │ └─────────────────────────┘ │
    │                            │   └─────────────────────────────┘
    │ ┌──────────────────────┐   │
    │ │ Background Tasks     │   │
    │ ├──────────────────────┤   │
    │ │ Price Listener       │   │
    │ │ Order Executor       │   │
    │ │ Risk Monitor         │   │
    │ │ Data Persister       │   │
    │ └──────────────────────┘   │
    │                            │
    │ ┌──────────────────────┐   │
    │ │ Database (SQLite)    │   │
    │ ├──────────────────────┤   │
    │ │ configs              │   │
    │ │ orders               │   │
    │ │ positions            │   │
    │ │ trades               │   │
    │ │ pnl_history          │   │
    │ └──────────────────────┘   │
    └────────────────────────────┘
```

### 3.2 数据流向

#### 启动流程
```
用户访问前端
    ↓
加载配置页面
    ↓
用户填写参数(交易对、资金、杠杆等)
    ↓
提交配置给后端 POST /api/config
    ↓
后端保存配置到数据库
    ↓
后端返回确认信息
    ↓
用户点击"启动策略"
    ↓
前端调用 POST /api/strategy/start
    ↓
后端初始化 GridStrategy 实例
    ↓
后端启动后台任务(价格监听、订单执行)
    ↓
前端建立 WebSocket 连接
    ↓
后端定时推送订单、价格、收益数据给前端
    ↓
前端实时渲染仪表板
```

#### 交易流程
```
1. 价格监听任务持续运行
    ↓
2. 查询 Backpack 最新价格
    ↓
3. 检查网格是否需要操作
    ↓
4a. 如果价格上升到卖点
    └─→ 执行平仓订单 (SELL)
        ↓
        获利 = (卖价 - 买价) × 数量
        ↓
        更新总收益
        ↓
        在底部重新挂买单
    ↓
4b. 如果价格下降到买点
    └─→ 执行建仓订单 (BUY)
        ↓
        增加持仓
        ↓
        更新平均建仓价格
    ↓
5. 每笔交易后检查风险
    ├─ 检查全局止损
    ├─ 检查全局止盈
    └─ 检查爆仓风险
    ↓
6. 如果触发止盈/止损
    ├─ 立即平仓所有头寸
    ├─ 清除所有挂单
    ├─ 标记策略为已停止
    └─ 推送通知给前端
    ↓
7. WebSocket 定时推送更新
    ├─ 当前价格
    ├─ 活跃订单
    ├─ 已平仓订单
    ├─ 总收益
    └─ 策略状态
```

---

## 功能需求

### 4.1 后端功能需求

#### 4.1.1 配置管理模块

- [ ] 保存用户配置(交易对、资金、杠杆、网格数等)
- [ ] 读取用户配置
- [ ] 验证配置参数的有效性
- [ ] 修改运行中的配置(仅部分参数)
- [ ] 配置版本管理(保存历史配置)

#### 4.1.2 网格策略模块

- [ ] 根据当前价格和参数自动计算网格价位
- [ ] 生成初始买单(底部分批建仓)
- [ ] 动态生成卖单(根据买入价格计算)
- [ ] 监听价格变化(通过 Backpack WebSocket)
- [ ] 判断价格是否触及网格点
- [ ] 执行买入/卖出操作

#### 4.1.3 订单管理模块

- [ ] 创建订单对象
- [ ] 追踪订单状态(待执行、待成交、已成交、已取消)
- [ ] 更新订单状态
- [ ] 关联成对的买卖订单(追踪单笔交易利润)
- [ ] 查询所有活跃订单
- [ ] 查询历史订单
- [ ] 批量取消订单

#### 4.1.4 头寸追踪模块

- [ ] 计算当前总头寸大小
- [ ] 计算平均建仓价格
- [ ] 计算浮动收益
- [ ] 计算已实现收益
- [ ] 追踪每个网格点的头寸信息

#### 4.1.5 风险管理模块

- [ ] 全局止损检查(总亏损达到上限时停止)
- [ ] 全局止盈检查(总收益达到目标时停止)
- [ ] 爆仓风险预警
- [ ] 单个网格最大损失限制
- [ ] 头寸风险率计算
- [ ] 自动平仓机制

#### 4.1.6 Backpack API 集成模块

- [ ] ED25519 签名生成(用于 API 认证)
- [ ] 查询市场信息
- [ ] 查询账户余额
- [ ] 查询头寸信息
- [ ] 执行下单 (POST /orders)
- [ ] 查询订单状态 (GET /orders)
- [ ] 取消订单 (DELETE /orders)
- [ ] 获取历史成交 (GET /fills)
- [ ] 连接 WebSocket 获取实时价格

#### 4.1.7 WebSocket 推送模块

- [ ] 建立与前端的 WebSocket 连接
- [ ] 实时推送当前价格
- [ ] 实时推送订单更新
- [ ] 实时推送收益数据
- [ ] 实时推送策略状态
- [ ] 错误和通知推送

#### 4.1.8 数据持久化模块

- [ ] 保存所有订单到数据库
- [ ] 保存配置到数据库
- [ ] 保存交易历史到数据库
- [ ] 保存每日收益统计
- [ ] 支持数据导出

#### 4.1.9 日志和监控模块

- [ ] 详细日志记录所有操作
- [ ] 区分 DEBUG/INFO/WARNING/ERROR 级别
- [ ] 记录 API 调用和响应
- [ ] 记录交易执行过程
- [ ] 错误追踪和报告

### 4.2 前端功能需求

#### 4.2.1 页面设计

**Dashboard 仪表板页面**
- [ ] 显示当前策略状态(运行中/已停止)
- [ ] 显示实时价格
- [ ] 显示总资金和已用资金
- [ ] 显示当前总头寸
- [ ] 显示总收益和收益率
- [ ] 显示止盈/止损目标
- [ ] 显示当前风险率

**Config 配置页面**
- [ ] 交易对选择(SOL_USDC_PERP / BTC_USDC_PERP / ETH_USDC_PERP)
- [ ] 资金输入(USDC 数量)
- [ ] 杠杆倍数选择(1x ~ 20x,建议 2x-5x)
- [ ] 网格数量设置(5 ~ 100)
- [ ] 价格区间设置(±5% ~ ±50%)
- [ ] 止损设置(金额)
- [ ] 止盈设置(金额)
- [ ] API Key 和 Secret Key 输入
- [ ] 保存/应用配置按钮
- [ ] 参数验证提示

**Orders 订单页面**
- [ ] 活跃订单表格(待成交的订单)
  - 订单 ID
  - 交易类型(BUY/SELL)
  - 价格
  - 数量
  - 委托时间
  - 状态
- [ ] 已成交订单表格
  - 买单价格
  - 卖单价格
  - 数量
  - 交易时间
  - 单笔利润
  - 累计利润
- [ ] 订单过滤和排序
- [ ] 订单详情弹窗

**Statistics 统计页面**
- [ ] 总成交笔数
- [ ] 获利笔数 / 亏损笔数
- [ ] 胜率
- [ ] 平均利润
- [ ] 最大单笔利润
- [ ] 最大单笔亏损
- [ ] 日收益曲线图
- [ ] 平均持仓时间

#### 4.2.2 交互功能

- [ ] 启动/停止策略按钮
- [ ] 紧急平仓按钮(一键清仓)
- [ ] 配置编辑保存
- [ ] 刷新实时数据
- [ ] 下载交易报告
- [ ] 表格分页和导出

#### 4.2.3 WebSocket 实时更新

- [ ] 自动连接 WebSocket
- [ ] 实时更新仪表板数据
- [ ] 实时更新订单表格
- [ ] 系统通知提醒(新订单、平仓、止盈/止损等)
- [ ] 自动重连机制

---

## 数据库设计

### 5.1 数据库选择

使用 **SQLite + SQLAlchemy** (可升级至 PostgreSQL)

### 5.2 数据表设计

#### 5.2.1 configs 表 - 交易配置

```sql
CREATE TABLE configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(50) NOT NULL,           -- 交易对,如 SOL_USDC_PERP
    leverage FLOAT NOT NULL,               -- 杠杆倍数
    total_capital FLOAT NOT NULL,          -- 总资金(USDC)
    grid_count INTEGER NOT NULL,           -- 网格数量
    price_range_percent FLOAT NOT NULL,    -- 价格区间百分比(±)
    max_total_loss FLOAT NOT NULL,         -- 全局止损(金额)
    target_profit FLOAT NOT NULL,          -- 全局止盈(金额)
    max_single_loss FLOAT,                 -- 单个网格最大亏损
    status VARCHAR(20),                    -- 配置状态:active/inactive
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

#### 5.2.2 orders 表 - 订单记录

```sql
CREATE TABLE orders (
    id VARCHAR(100) PRIMARY KEY,           -- Backpack 订单 ID
    symbol VARCHAR(50) NOT NULL,           -- 交易对
    side VARCHAR(10) NOT NULL,             -- BUY / SELL
    order_type VARCHAR(20) NOT NULL,       -- Limit / Market
    price FLOAT NOT NULL,                  -- 订单价格
    quantity FLOAT NOT NULL,               -- 订单数量
    executed_quantity FLOAT,               -- 已成交数量
    status VARCHAR(20) NOT NULL,           -- Pending / Filled / Cancelled
    grid_level INTEGER,                    -- 网格层级(用于关联)
    paired_order_id VARCHAR(100),          -- 配对的订单 ID(买卖对)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    filled_at TIMESTAMP,
    average_fill_price FLOAT,              -- 平均成交价
    commission FLOAT,                      -- 手续费
    pnl FLOAT,                             -- 该笔交易的损益
    notes TEXT
);

CREATE INDEX idx_orders_symbol ON orders(symbol);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

#### 5.2.3 positions 表 - 头寸跟踪

```sql
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(50) NOT NULL,           -- 交易对
    size FLOAT NOT NULL,                   -- 当前头寸大小
    average_price FLOAT NOT NULL,          -- 平均建仓价格
    side VARCHAR(10),                      -- LONG / SHORT
    entry_time TIMESTAMP,                  -- 建仓时间
    current_price FLOAT,                   -- 当前市场价格
    unrealized_pnl FLOAT,                  -- 未实现收益
    realized_pnl FLOAT,                    -- 已实现收益
    margin_used FLOAT,                     -- 占用保证金
    liquidation_price FLOAT,               -- 清算价格
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.2.4 trades 表 - 交易历史

```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(50) NOT NULL,           -- 交易对
    buy_order_id VARCHAR(100),             -- 买单 ID
    sell_order_id VARCHAR(100),            -- 卖单 ID
    buy_price FLOAT NOT NULL,              -- 买入价格
    sell_price FLOAT NOT NULL,             -- 卖出价格
    quantity FLOAT NOT NULL,               -- 成交数量
    profit_per_unit FLOAT,                 -- 单位利润
    total_profit FLOAT,                    -- 总利润
    fee FLOAT,                             -- 总手续费
    net_profit FLOAT,                      -- 净利润
    pnl_percent FLOAT,                     -- 利润率 %
    entry_time TIMESTAMP,                  -- 建仓时间
    exit_time TIMESTAMP,                   -- 平仓时间
    hold_duration INTEGER,                 -- 持仓时长(秒)
    notes TEXT
);

CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_exit_time ON trades(exit_time);
```

#### 5.2.5 pnl_history 表 - 收益历史

```sql
CREATE TABLE pnl_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(50) NOT NULL,
    trade_date DATE NOT NULL,              -- 交易日期
    total_trades INTEGER,                  -- 总交易笔数
    winning_trades INTEGER,                -- 获利笔数
    losing_trades INTEGER,                 -- 亏损笔数
    total_profit FLOAT,                    -- 总利润
    realized_profit FLOAT,                 -- 已实现利润
    unrealized_profit FLOAT,               -- 未实现利润
    win_rate FLOAT,                        -- 胜率 %
    avg_profit_per_trade FLOAT,            -- 平均每笔利润
    max_single_profit FLOAT,               -- 最大单笔利润
    max_single_loss FLOAT,                 -- 最大单笔亏损
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5.2.6 strategy_state 表 - 策略状态

```sql
CREATE TABLE strategy_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status VARCHAR(20),                    -- RUNNING / STOPPED / PAUSED / ERROR
    start_time TIMESTAMP,                  -- 策略启动时间
    stop_time TIMESTAMP,                   -- 策略停止时间
    stop_reason VARCHAR(50),               -- 停止原因:MANUAL / PROFIT_TARGET / LOSS_LIMIT / ERROR
    total_capital FLOAT,                   -- 初始资金
    current_balance FLOAT,                 -- 当前余额
    total_realized_profit FLOAT,           -- 总已实现利润
    total_unrealized_profit FLOAT,         -- 总未实现利润
    grid_buy_orders INTEGER,               -- 活跃买单数
    grid_sell_orders INTEGER,              -- 活跃卖单数
    current_grid_level INTEGER,            -- 当前网格层级
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5.3 数据库初始化脚本

```python
# backend/db/init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading_bot.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """初始化数据库所有表"""
    Base.metadata.create_all(bind=engine)
```

---

## API 设计

### 6.1 后端 REST API 端点

#### 6.1.1 配置管理接口

**POST /api/config**
```
请求:
{
    "symbol": "SOL_USDC_PERP",
    "leverage": 2,
    "total_capital": 500,
    "grid_count": 10,
    "price_range_percent": 10,
    "max_total_loss": 100,
    "target_profit": 300,
    "max_single_loss": 50
}

响应:
{
    "code": 0,
    "message": "配置保存成功",
    "data": {
        "config_id": 1,
        "created_at": "2025-10-23T10:00:00Z"
    }
}
```

**GET /api/config**
```
响应:
{
    "code": 0,
    "data": {
        "symbol": "SOL_USDC_PERP",
        "leverage": 2,
        "total_capital": 500,
        ...
    }
}
```

#### 6.1.2 策略控制接口

**POST /api/strategy/start**
```
请求:{}

响应:
{
    "code": 0,
    "message": "策略已启动",
    "data": {
        "status": "RUNNING",
        "start_time": "2025-10-23T10:00:00Z",
        "grid_prices": [180, 184, 188, ...]
    }
}
```

**POST /api/strategy/stop**
```
请求:{}

响应:
{
    "code": 0,
    "message": "策略已停止",
    "data": {
        "status": "STOPPED",
        "stop_time": "2025-10-23T10:30:00Z",
        "total_profit": 45.50
    }
}
```

**POST /api/strategy/emergency-close**
```
请求:{}

响应(一键平仓所有头寸):
{
    "code": 0,
    "message": "紧急平仓已执行",
    "data": {
        "closed_positions": 3,
        "total_pnl": 45.50
    }
}
```

#### 6.1.3 订单查询接口

**GET /api/orders?status=pending&limit=20**
```
响应:
{
    "code": 0,
    "data": {
        "total": 5,
        "orders": [
            {
                "order_id": "12345",
                "symbol": "SOL_USDC_PERP",
                "side": "BUY",
                "price": 139.5,
                "quantity": 3.5,
                "status": "PENDING",
                "created_at": "2025-10-23T10:00:00Z"
            },
            ...
        ]
    }
}
```

**GET /api/trades?limit=50**
```
响应:
{
    "code": 0,
    "data": {
        "total": 18,
        "trades": [
            {
                "id": 1,
                "buy_price": 140.5,
                "sell_price": 142.0,
                "quantity": 3.5,
                "profit": 5.25,
                "entry_time": "2025-10-23T09:30:00Z",
                "exit_time": "2025-10-23T09:45:00Z"
            },
            ...
        ]
    }
}
```

#### 6.1.4 头寸查询接口

**GET /api/positions**
```
响应:
{
    "code": 0,
    "data": {
        "symbol": "SOL_USDC_PERP",
        "size": 7.0,
        "average_price": 140.5,
        "side": "LONG",
        "current_price": 141.2,
        "unrealized_pnl": 4.90,
        "margin_used": 490,
        "margin_available": 10
    }
}
```

#### 6.1.5 统计信息接口

**GET /api/statistics**
```
响应:
{
    "code": 0,
    "data": {
        "total_capital": 500,
        "current_balance": 545.50,
        "total_profit": 45.50,
        "total_profit_percent": 9.1,
        "total_trades": 18,
        "winning_trades": 15,
        "losing_trades": 3,
        "win_rate": 83.3,
        "avg_profit_per_trade": 2.53,
        "max_single_profit": 5.25,
        "max_single_loss": -2.10,
        "started_at": "2025-10-23T08:00:00Z",
        "strategy_status": "RUNNING"
    }
}
```

#### 6.1.6 系统状态接口

**GET /api/status**
```
响应:
{
    "code": 0,
    "data": {
        "strategy_status": "RUNNING",
        "backpack_api_connected": true,
        "websocket_connected": true,
        "database_status": "OK",
        "current_price": 141.2,
        "timestamp": "2025-10-23T10:25:30Z"
    }
}
```

### 6.2 WebSocket 事件定义

**WebSocket 连接** `ws://localhost:8000/ws`

**客户端发送事件**:

```javascript
// 订阅订单更新
{ type: "subscribe", channel: "orders" }

// 订阅价格更新
{ type: "subscribe", channel: "prices" }

// 订阅统计信息
{ type: "subscribe", channel: "statistics" }

// 心跳保活
{ type: "ping" }
```

**服务器推送事件**:

```javascript
// 新订单创建
{
    type: "order_created",
    data: {
        order_id: "12345",
        side: "BUY",
        price: 139.5,
        quantity: 3.5,
        timestamp: "2025-10-23T10:25:30Z"
    }
}

// 订单成交
{
    type: "order_filled",
    data: {
        order_id: "12345",
        filled_quantity: 3.5,
        average_price: 139.52,
        timestamp: "2025-10-23T10:25:35Z"
    }
}

// 价格更新
{
    type: "price_update",
    data: {
        symbol: "SOL_USDC_PERP",
        price: 141.25,
        bid: 141.20,
        ask: 141.30,
        timestamp: "2025-10-23T10:25:40Z"
    }
}

// 交易完成(买卖对配对)
{
    type: "trade_completed",
    data: {
        buy_order_id: "12345",
        sell_order_id: "12346",
        entry_price: 139.5,
        exit_price: 142.0,
        quantity: 3.5,
        profit: 5.25,
        pnl_percent: 1.88,
        timestamp: "2025-10-23T10:25:45Z"
    }
}

// 策略状态变更
{
    type: "strategy_status_changed",
    data: {
        status: "STOPPED",
        reason: "PROFIT_TARGET_REACHED",
        final_profit: 45.50,
        timestamp: "2025-10-23T10:30:00Z"
    }
}

// 风险警告
{
    type: "risk_warning",
    data: {
        message: "接近止损线",
        current_loss": -95.0,
        loss_limit": -100,
        timestamp: "2025-10-23T10:25:50Z"
    }
}

// 错误通知
{
    type: "error",
    data: {
        message: "API 调用失败",
        error_code": 429,
        timestamp: "2025-10-23T10:26:00Z"
    }
}

// 心跳响应
{ type: "pong" }
```

---

## 前端设计

### 7.1 页面布局

#### 7.1.1 Dashboard 仪表板

```
┌─────────────────────────────────────────────────────────┐
│ 网格交易机器人 Dashboard                   [启动] [停止] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 策略状态     │ 当前价格     │ 总资金       │          │
│ │ 运行中       │ $141.25      │ 500 USDC     │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 总收益       │ 收益率       │ 风险率       │          │
│ │ +$45.50      │ +9.1%        │ 22%          │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 已用保证金   │ 可用保证金   │ 当前头寸     │          │
│ │ $490.00      │ $10.00       │ 7.0 SOL      │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ 止盈/止损目标 ████░░░░░░ $45.50 / $300.00             │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 活跃订单 (5)                                        │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ 类型  价格    数量    状态    委托时间        │ │
│ │ BUY   139.5  3.5    PENDING  14:32:10       │ │
│ │ SELL  143.2  3.5    PENDING  14:15:32       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 收益曲线                                            │ │
│ │ [图表区域 - 日收益变化]                             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### 7.1.2 Config 配置页面

```
┌─────────────────────────────────────────────────────────┐
│ 交易配置                                   [保存] [应用] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 基础参数                                                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 交易对:[SOL_USDC_PERP ▼]                          │ │
│ │                                                     │ │
│ │ 资金:[500        ] USDC                            │ │
│ │                                                     │ │
│ │ 杠杆:[2  ▼] (1x ~ 20x,建议 2x-5x)               │ │
│ │                                                     │ │
│ │ 网格数:[10        ]                                │ │
│ │                                                     │ │
│ │ 价格区间:[±10      ] %                             │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ 风险管理                                                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 全局止损:[-100         ] USDC 负数表示亏损金额      │ │
│ │                                                     │ │
│ │ 全局止盈:[+300         ] USDC 正数表示获利金额      │ │
│ │                                                     │ │
│ │ 单个网格最大亏损:[-50         ] USDC               │ │
│ │                                                     │ │
│ │ ☑ 启用自动止损                                     │ │
│ │ ☑ 启用爆仓保护                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ API 凭证                                                │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ API Key: [****************************]            │ │
│ │                                                     │ │
│ │ Secret Key: [****************************]         │ │
│ │                                                     │ │
│ │ [✓ 连接测试]                                        │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

#### 7.1.3 Orders 订单页面

**标签页 1:活跃订单**
```
┌─────────────────────────────────────────────────────────┐
│ 活跃订单 (5)                     [刷新] [全部取消]       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  订单ID   类型  价格   数量   状态    委托时间     操作  │
│  ────────────────────────────────────────────────────── │
│  12345   BUY   139.5 3.5  PENDING 14:32:10  [取消]  │
│  12346   BUY   137.0 3.5  PENDING 14:28:45  [取消]  │
│  12347   SELL  143.2 3.5  PENDING 14:15:32  [取消]  │
│  12348   SELL  145.7 3.5  PENDING 14:10:15  [取消]  │
│  12349   BUY   134.5 3.5  PENDING 13:56:00  [取消]  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**标签页 2:已成交订单**
```
┌─────────────────────────────────────────────────────────┐
│ 已成交订单 (18)                   [导出] [筛选]          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 买价   卖价   数量  成交时间    单笔利润  累计利润       │
│ ─────────────────────────────────────────────────────  │
│ 140.5 142.0  3.5  14:22:15   +$5.25   +$85.30      │
│ 137.8 140.5  3.5  14:08:30   +$8.10   +$80.05      │
│ 135.2 137.0  3.5  13:45:20   +$6.30   +$71.95      │
│ 142.0 143.5  3.5  13:25:10   +$5.25   +$65.65      │
│ 139.5 142.0  3.5  13:05:00   +$7.50   +$60.40      │
│ ...                                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 7.1.4 Statistics 统计页面

```
┌─────────────────────────────────────────────────────────┐
│ 交易统计                                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 关键指标                                                │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 总交易笔数   │ 获利笔数     │ 亏损笔数     │          │
│ │ 18           │ 15           │ 3            │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 胜率         │ 平均利润     │ 最大利润     │          │
│ │ 83.3%        │ +$2.53       │ +$8.10       │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ ┌──────────────┬──────────────┬──────────────┐          │
│ │ 最大亏损     │ 平均持仓时间 │ 总持仓时长   │          │
│ │ -$2.10       │ 16分钟       │ 4小时23分    │          │
│ └──────────────┴──────────────┴──────────────┘          │
│                                                         │
│ 日收益走势                                              │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [折线图:X轴为日期,Y轴为收益金额]                   │ │
│ │                                                     │ │
│ │     $50 ┤     ╱╲      ╱╲                            │ │
│ │     $40 ├    ╱  ╲    ╱  ╲  ╱╲                       │ │
│ │     $30 ├   ╱    ╲  ╱    ╲╱  ╲                      │ │
│ │     $20 ├  ╱      ╲╱          ╲                     │ │
│ │     $10 ├─┼───────────────────────────→            │ │
│ │         └────────────────────────────────           │ │
│ │          10/21 10/22 10/23 10/24 10/25            │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 7.2 技术实现细节

#### 7.2.1 状态管理(Zustand Store)

```typescript
// store/trading.ts
import { create } from 'zustand';

interface TradingStore {
  // 策略状态
  strategy: {
    status: 'IDLE' | 'RUNNING' | 'STOPPED' | 'ERROR';
    startTime: string | null;
    stopTime: string | null;
  };

  // 配置
  config: {
    symbol: string;
    leverage: number;
    totalCapital: number;
    gridCount: number;
    priceRangePercent: number;
    maxTotalLoss: number;
    targetProfit: number;
  };

  // 实时数据
  realtime: {
    currentPrice: number;
    totalProfit: number;
    profitPercent: number;
    activeOrders: Order[];
    currentPosition: Position;
  };

  // 订单和交易历史
  trades: Trade[];
  statistics: Statistics;

  // Actions
  updateStrategy: (data: any) => void;
  updateRealtime: (data: any) => void;
  addTrade: (trade: Trade) => void;
}

export const useTradingStore = create<TradingStore>((set) => ({
  // ... 实现
}));
```

#### 7.2.2 WebSocket 客户端

```typescript
// lib/websocket-client.ts
import { useEffect } from 'react';
import { useTradingStore } from '@/store/trading';

export const useWebSocketClient = () => {
  const store = useTradingStore();
  
  useEffect(() => {
    const ws = new WebSocket(`ws://${process.env.NEXT_PUBLIC_API_URL}/ws`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      // 订阅频道
      ws.send(JSON.stringify({ type: 'subscribe', channel: 'all' }));
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'price_update':
          store.updateRealtime({ currentPrice: message.data.price });
          break;
        case 'order_filled':
          // 更新订单表格
          break;
        case 'trade_completed':
          store.addTrade(message.data);
          break;
        // ... 其他事件处理
      }
    };

    return () => ws.close();
  }, []);
};
```

---

## 后端逻辑

### 8.1 网格策略核心逻辑

#### 8.1.1 初始化流程

```python
# backend/core/grid_strategy.py
class GridStrategy:
    def __init__(self, config: Config, backpack_client: BackpackClient):
        self.config = config
        self.backpack_client = backpack_client
        self.grid_prices = []
        self.active_orders = {}
        self.position_tracker = PositionTracker()
        self.risk_manager = RiskManager(config)
        
    async def initialize(self):
        """初始化网格"""
        # 1. 获取当前价格
        current_price = await self.backpack_client.get_last_price(self.config.symbol)
        
        # 2. 计算网格价位
        self.grid_prices = self._calculate_grid_prices(
            current_price,
            self.config.price_range_percent,
            self.config.grid_count
        )
        
        # 3. 生成初始买单
        await self._place_initial_buy_orders()
        
        # 4. 启动后台监听任务
        asyncio.create_task(self._price_listener_loop())
        asyncio.create_task(self._risk_monitor_loop())
        
    def _calculate_grid_prices(self, current_price, range_percent, grid_count):
        """计算网格价位"""
        range_amount = current_price * range_percent / 100
        bottom_price = current_price - range_amount
        top_price = current_price + range_amount
        step = (top_price - bottom_price) / (grid_count - 1)
        
        return [bottom_price + i * step for i in range(grid_count)]
    
    async def _place_initial_buy_orders(self):
        """在底部分批下买单"""
        # 每个网格的仓位大小
        qty_per_grid = self.config.total_capital / self.config.grid_count / self.grid_prices[0]
        
        for i, price in enumerate(self.grid_prices[:self.config.grid_count // 2]):
            order = await self.backpack_client.place_order(
                symbol=self.config.symbol,
                side='Bid',  # BUY
                order_type='Limit',
                price=price,
                quantity=qty_per_grid
            )
            self.active_orders[order.id] = order
            logger.info(f"初始买单已下达:ID={order.id}, 价格={price}, 数量={qty_per_grid}")
```

#### 8.1.2 价格监听和交易执行

```python
async def _price_listener_loop(self):
    """持续监听价格变化"""
    async for price_data in self.backpack_client.price_stream(self.config.symbol):
        current_price = price_data['price']
        
        # 检查是否触及网格点
        triggered_grids = self._check_grid_triggers(current_price)
        
        for grid_info in triggered_grids:
            if grid_info['direction'] == 'UP':
                # 价格上升到卖点 → 平仓
                await self._execute_sell(grid_info)
            elif grid_info['direction'] == 'DOWN':
                # 价格下降到买点 → 加仓
                await self._execute_buy(grid_info)

async def _execute_sell(self, grid_info):
    """执行平仓(卖出)"""
    # 1. 查找对应的买单
    buy_order = self._find_paired_buy_order(grid_info)
    
    # 2. 计算卖单数量和价格
    qty = buy_order.executed_quantity
    sell_price = grid_info['price']
    
    # 3. 下卖单
    sell_order = await self.backpack_client.place_order(
        symbol=self.config.symbol,
        side='Ask',  # SELL
        order_type='Limit',
        price=sell_price,
        quantity=qty
    )
    
    # 4. 关联买卖订单
    self._link_orders(buy_order.id, sell_order.id)
    
    # 5. 计算获利
    profit = (sell_price - buy_order.average_price) * qty
    logger.info(f"平仓订单已下达:profit={profit}")
    
    # 6. 在底部重新下买单(继续网格)
    await self._place_replacement_buy_order()
```

#### 8.1.3 风险管理

```python
async def _risk_monitor_loop(self):
    """持续监控风险"""
    while self.is_running:
        # 1. 检查全局止损
        total_loss = self.position_tracker.total_realized_loss
        if total_loss <= -self.config.max_total_loss:
            logger.warning(f"触发全局止损!总亏损:{total_loss}")
            await self.stop('LOSS_LIMIT')
            return
        
        # 2. 检查全局止盈
        total_profit = self.position_tracker.total_realized_profit
        if total_profit >= self.config.target_profit:
            logger.info(f"触发全局止盈!总获利:{total_profit}")
            await self.stop('PROFIT_TARGET')
            return
        
        # 3. 检查爆仓风险
        leverage_ratio = self.risk_manager.calculate_leverage_ratio()
        if leverage_ratio > 0.8:
            logger.warning(f"杠杆比率过高:{leverage_ratio}")
            # 触发自动平仓或警告
        
        await asyncio.sleep(5)  # 每 5 秒检查一次

async def stop(self, reason='MANUAL'):
    """停止策略并清仓"""
    logger.info(f"策略停止,原因:{reason}")
    
    # 1. 取消所有未成交订单
    await self._cancel_all_pending_orders()
    
    # 2. 平仓所有头寸
    await self._close_all_positions()
    
    # 3. 记录最终数据到数据库
    await self._persist_final_state(reason)
    
    self.is_running = False
```

---

## 风险管理

### 9.1 风险管理策略

#### 9.1.1 全局止损 (Global Stop Loss)

- **触发条件**:已实现亏损 ≥ 配置的最大亏损额
- **执行动作**:
  1. 立即取消所有未成交订单
  2. 平仓所有开仓头寸
  3. 停止策略,记录日志
- **用户配置**:`max_total_loss = -100 USDC`

#### 9.1.2 全局止盈 (Global Take Profit)

- **触发条件**:已实现收益 ≥ 配置的目标收益额
- **执行动作**:
  1. 立即取消所有未成交订单
  2. 平仓所有开仓头寸
  3. 停止策略,记录日志
- **用户配置**:`target_profit = 300 USDC`

#### 9.1.3 单个网格最大亏损

- **触发条件**:单个交易对的亏损 ≥ 最大亏损额
- **执行动作**:跳过该网格点,转移资金到其他点
- **用户配置**:`max_single_loss = -50 USDC`

#### 9.1.4 爆仓保护

- **风险率计算**:`风险率 = 头寸保证金 / 总资金`
- **预警线**:风险率 > 50%
- **止损线**:风险率 > 75%,自动平仓一部分头寸
- **爆仓线**:风险率 > 95%,紧急平仓所有

#### 9.1.5 价格滑点保护

- 下单时设置最大滑点限制
- 如果成交价超过滑点,订单自动取消

---

## 部署方案

### 10.1 本地开发环境

#### 10.1.1 后端启动

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/grid-trading-bot.git
cd grid-trading-bot

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
cd backend
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env,填入 Backpack API Key 和 Secret Key

# 5. 初始化数据库
python -c "from db.init_db import init_db; init_db()"

# 6. 启动后端服务
uvicorn app:app --reload --port 8000
```

#### 10.1.2 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env.local
# 编辑 .env.local,设置 NEXT_PUBLIC_API_URL

# 4. 启动开发服务器
npm run dev

# 5. 访问 http://localhost:3000
```

### 10.2 Docker 容器部署

#### 10.2.1 后端 Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 10.2.2 前端 Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

#### 10.2.3 Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./trading_bot.db
      - BACKPACK_API_KEY=${BACKPACK_API_KEY}
      - BACKPACK_SECRET_KEY=${BACKPACK_SECRET_KEY}
    volumes:
      - ./backend:/app
      - trading_data:/app/data
    command: uvicorn app:app --host 0.0.0.0 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

volumes:
  trading_data:
```

**启动所有服务**:
```bash
docker-compose up -d
```

---

## 开发计划

### 11.1 第一阶段:核心交易引擎(第 1-2 周)

**后端**
- [x] FastAPI 项目初始化
- [x] SQLAlchemy 数据库设置
- [x] Backpack API 客户端实现
- [x] 订单管理模块
- [x] 网格价位计算
- [x] 初始建仓逻辑

**前端**
- [x] Next.js 项目初始化
- [x] 基础页面框架
- [x] 配置表单

**测试**
- [ ] 单元测试(后端核心逻辑)
- [ ] API 集成测试

### 11.2 第二阶段:自动交易和监控(第 3-4 周)

**后端**
- [ ] 价格监听任务
- [ ] 自动交易执行
- [ ] WebSocket 推送
- [ ] 风险管理模块
- [ ] 数据持久化

**前端**
- [ ] 仪表板页面
- [ ] 订单表格
- [ ] WebSocket 实时更新
- [ ] 状态管理(Zustand)

**测试**
- [ ] 模拟交易测试
- [ ] 风险管理测试

### 11.3 第三阶段:优化和部署(第 5-6 周)

**后端**
- [ ] 错误处理和日志
- [ ] 性能优化
- [ ] API 限流
- [ ] 认证授权

**前端**
- [ ] UI/UX 优化
- [ ] 响应式设计
- [ ] 性能优化

**部署**
- [ ] Docker 容器化
- [ ] 生产环境配置
- [ ] 监控和告警

### 11.4 里程碑

| 阶段 | 目标 | 完成时间 |
|------|------|--------|
| MVP | 完整的网格交易流程,支持启动和停止 | 第 2 周 |
| Beta | 全部风险管理功能,稳定性达 99% | 第 4 周 |
| Release | 生产环境就绪,支持部署 | 第 6 周 |

---

## 附录

### A.1 常见问题解答 (FAQ)

**Q: 如何保护 API Key?**  
A: 使用环境变量存储,不要提交到代码库。使用 .env 文件和 .gitignore 保护。

**Q: 网格数量多少合适?**  
A: 建议 5-20 个。太多会增加交易成本,太少可能错过机会。

**Q: 杠杆多少比较安全?**  
A: 初学者建议 2-3x,风险承受能力强可用 5-10x,不建议超过 10x。

**Q: 如何应对单边行情?**  
A: 设置止损线,价格突破网格范围时自动停止。

**Q: 手续费如何计算?**  
A: Backpack Maker 费 0.02%,Taker 费 0.05%。单笔交易手续费 = 交易额 × 费率。

---

**文档版本**:v1.0  
**最后更新**:2025-10-23  
**维护者**:Team Dev
