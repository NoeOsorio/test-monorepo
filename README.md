# Simple Monorepo

A minimal monorepo with Vite (React) frontend and Flask backend for testing cloud deployments.

## Structure

```
├── frontend/    # Vite + React app (port 3000)
└── backend/     # Flask API (port 5000)
```

## Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

**Frontend:**
- `VITE_API_URL` - Backend API URL (default: http://localhost:5001)


