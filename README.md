# Simple Monorepo

A minimal monorepo with Vite (React) frontend and Flask backend for testing cloud deployments.

## Structure

```
├── frontend/    # Vite + React app (port 3000)
└── backend/     # Flask API (port 5051)
```

## Running Locally

### Backend

#### Prerequisites

- Python 3.x
- PostgreSQL database (can be run via Docker Compose)

#### Option 1: Using Docker Compose (Recommended)

```bash
docker-compose up
```

This will start both PostgreSQL and the backend service.

#### Option 2: Manual Setup

1. **Start PostgreSQL database:**

   ```bash
   docker-compose up postgres
   ```

2. **Set up environment variables:**

   ```bash
   cd backend
   cp env.example .env
   ```

   Edit `.env` with your database credentials if needed.

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:5051`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

**Backend:**

- `DB_URL` - PostgreSQL connection URL (e.g., `postgresql://user:pass@host:port/dbname`)
- `DB_HOST` - Database host (default: `localhost`)
- `DB_PORT` - Database port (default: `5432`)
- `DB_NAME` - Database name (default: `postgres`)
- `DB_USER` - Database user (default: `postgres`)
- `DB_PASS` - Database password (default: `postgres`)
- `FLASK_ENV` - Flask environment (default: `development`)

**Note:** You can use either `DB_URL` directly or the individual `DB_*` variables. If `DB_URL` is set, it takes precedence.

> Testing Actions, please delete later

**Frontend:**

- `VITE_API_URL` - Backend API URL (default: http://localhost:5051)

Test
