# Simple Monorepo

A minimal monorepo with Vite (React) frontend and Flask backend for testing cloud deployments.

## Structure

```
├── frontend/    # Vite + React app (port 3000)
└── backend/     # Flask API (port 5051)
```

## Running Locally

### Backend (dev)

#### Prerequisites

- Python 3.x
- PostgreSQL database (can be run via Docker Compose)

#### Option 1: Docker Compose (recommended)

```bash
docker compose up --build
```

This starts PostgreSQL and the backend service (no frontend).

#### Option 2: Manual (Python)

1. **Start PostgreSQL database:**

   ```bash
   docker compose up postgres
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

### Frontend (dev)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Production-style runs

### Backend (prod)

#### Option 1: Run the Docker image (matches `backend/Dockerfile`)

```bash
cp backend/env.example backend/.env
docker build -t monorepo-backend ./backend
docker run --rm -p 5051:5051 --env-file backend/.env monorepo-backend
```

#### Option 2: Run with Gunicorn (WSGI server)

```bash
cd backend
pip install -r requirements.txt
gunicorn -b 0.0.0.0:5051 --access-logfile - --error-logfile - --capture-output app:app
```

### Frontend (prod)

```bash
cd frontend
npm install
npm run build
npm run preview -- --host 0.0.0.0 --port 3000
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

**Frontend:**

- `VITE_API_URL` - Backend API URL (default: http://localhost:5051)

## Jobs and Workers

Test scripts and workers for deployment testing:

```bash
bash jobs/funny-message.sh
bash jobs/failed-script.sh
bash jobs/funny-worker.sh
bash jobs/failed-worker.sh
```
