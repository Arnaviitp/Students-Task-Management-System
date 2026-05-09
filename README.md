# Student Task Manager (Nuxt + FastAPI)

A simple student task manager that lets you create, manage, and track tasks.

## Tech

- Frontend: Nuxt (v4 target)
- Backend: FastAPI + SQLite

## Quickstart (dev)

### 1) Backend (FastAPI)

```powershell
cd D:\git\Website\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be at `http://127.0.0.1:8000` (OpenAPI docs at `/docs`).

### 2) Frontend (Nuxt)

```powershell
cd D:\git\Website\frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

Frontend will be at `http://127.0.0.1:3000`.

## Config

- Backend DB path: `backend/.data/tasks.db` (auto-created)
- Frontend API base: set `NUXT_PUBLIC_API_BASE` (defaults to `http://127.0.0.1:8000`)
