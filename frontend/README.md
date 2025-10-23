# Grid Trading Bot - Frontend

This is the frontend application for the Grid Trading Bot built with Next.js.

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Charts**: Recharts
- **Tables**: TanStack Table
- **Forms**: React Hook Form + Zod

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local to set the API URL
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── lib/              # Utilities and helpers
│   └── types/            # TypeScript type definitions
├── public/               # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Features

- **Dashboard**: Real-time trading strategy monitoring
- **Configuration**: Easy setup of trading parameters
- **Orders**: View and manage orders
- **Statistics**: Performance metrics and analytics

## Documentation

Full project documentation is available in `docs/PROJECT_DOCUMENTATION.md`
