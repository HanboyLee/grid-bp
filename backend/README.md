# Grid Trading Bot - Backend

This is the backend API for the Grid Trading Bot targeting the Backpack Exchange.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: SQLite + SQLAlchemy (async)
- **Python**: 3.10+

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Backpack API credentials
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── crud/             # Database operations
│   ├── db/               # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   ├── config.py         # Configuration management
│   └── main.py           # FastAPI app entry point
├── requirements.txt
├── Dockerfile
└── .env.example
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/config` - Save trading configuration
- `GET /api/config` - Get active configuration
- `POST /api/strategy/start` - Start trading strategy
- `POST /api/strategy/stop` - Stop trading strategy
- `POST /api/strategy/emergency-close` - Emergency close all positions
- `GET /api/orders` - List orders
- `GET /api/status` - Get system status

## Documentation

Full project documentation is available in `docs/PROJECT_DOCUMENTATION.md`

## Development

The project follows these code practices:

- **Type hints**: All functions use Python type hints
- **Async/await**: All I/O operations are async
- **Dependency injection**: FastAPI's dependency system is used
- **Separation of concerns**: Clear separation between API, business logic, and data layers
- **Error handling**: Proper error handling with meaningful messages
- **Logging**: Comprehensive logging for debugging and monitoring
