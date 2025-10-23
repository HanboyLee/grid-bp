# Grid Trading Bot for Backpack Exchange

This repository implements an automated perpetual futures grid trading bot for the Backpack exchange.

## 📖 Documentation

- **Full Project Documentation**: [`docs/PROJECT_DOCUMENTATION.md`](docs/PROJECT_DOCUMENTATION.md)
- **Backend README**: [`backend/README.md`](backend/README.md)
- **Frontend README**: [`frontend/README.md`](frontend/README.md)

## 🏗️ Project Structure

```
grid-trading-bot/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── crud/           # Database operations
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Next.js TypeScript frontend
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities
│   │   └── styles/        # Global styles
│   ├── package.json
│   └── Dockerfile
├── docs/                   # Project documentation
├── docker-compose.yml      # Docker orchestration
└── README.md
```

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd grid-trading-bot

# Set up environment variables
cp .env.example .env
# Edit .env with your Backpack API credentials

# Start all services
docker-compose up -d

# Access the application
# Backend API: http://localhost:8000
# Frontend UI: http://localhost:3000
```

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local to set API URL
npm run dev
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLite + SQLAlchemy (async)
- **Language**: Python 3.10+
- **Key Libraries**: Pydantic, httpx, websockets, cryptography

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charts**: Recharts
- **Tables**: TanStack Table

## 📋 Features

- ✅ **Trading Configuration**: Web-based parameter setup
- ✅ **Automated Grid Generation**: Calculate grid levels automatically
- ✅ **Order Management**: Track and manage orders
- ✅ **Risk Management**: Stop loss and take profit mechanisms
- ✅ **Position Tracking**: Monitor open positions
- ✅ **Real-time Updates**: WebSocket integration (planned)
- ✅ **Performance Statistics**: Track P&L and win rate (planned)

## 🔧 Code Practices

This project follows these coding practices:

### Backend (Python)
- **Type Hints**: All functions use Python type hints for better code quality
- **Async/Await**: All I/O operations are asynchronous for better performance
- **Dependency Injection**: FastAPI's dependency system for clean architecture
- **Separation of Concerns**: Clear separation between API, business logic, and data layers
- **Pydantic Validation**: Request/response validation using Pydantic models
- **Logging**: Comprehensive logging with proper log levels
- **Error Handling**: Proper exception handling with meaningful error messages

### Frontend (TypeScript)
- **TypeScript**: Full type safety across the application
- **Component-based**: Reusable React components
- **Modern React**: Using React hooks and Next.js 14 app directory
- **Tailwind CSS**: Utility-first styling approach
- **Responsive Design**: Mobile-friendly layouts

## 📊 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/config` - Save trading configuration
- `GET /api/config` - Get active configuration
- `POST /api/strategy/start` - Start trading strategy
- `POST /api/strategy/stop` - Stop trading strategy
- `POST /api/strategy/emergency-close` - Emergency close
- `GET /api/orders` - List orders
- `GET /api/status` - System status

## 🔐 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./trading_bot.db
BACKPACK_API_KEY=your_api_key_here
BACKPACK_SECRET_KEY=your_secret_key_here
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🧪 Development Status

This project is in active development following the phases outlined in the project documentation:

- ✅ Phase 1: Core backend structure and database models
- ✅ Phase 1: API endpoints and basic services
- ✅ Phase 1: Frontend structure and basic pages
- 🔄 Phase 2: Trading strategy implementation
- 🔄 Phase 2: Real-time WebSocket updates
- ⏳ Phase 3: Advanced features and optimization

## 📝 License

See project documentation for license information.

## 🤝 Contributing

Contributions are welcome! Please follow the coding practices outlined in this README and the project documentation.

## ⚠️ Disclaimer

This is a trading bot that can execute real trades. Use at your own risk. Always test with small amounts first and understand the risks involved in automated trading.
