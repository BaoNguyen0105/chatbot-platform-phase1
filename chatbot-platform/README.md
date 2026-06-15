# Chatbot Platform — Phase 1: Foundation

## Stack
- FastAPI + SQLAlchemy 2.0 + Alembic
- PostgreSQL 16 (with `pgvector` extension pre-enabled for Phase 4)
- JWT auth (access + refresh tokens)

## 1. Start PostgreSQL

```bash
docker compose up -d
```

This starts Postgres on `localhost:5432` with db `chatbot_db`, user `chatbot_user`, password `chatbot_pass`, and enables `uuid-ossp`, `vector`, `pg_trgm` extensions.

## 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # edit JWT_SECRET_KEY etc.
```

## 3. Run migrations

```bash
alembic revision --autogenerate -m "init schema"
alembic upgrade head
```

## 4. Run the API

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Endpoints in this phase

| Method | Path                | Auth | Description                        |
|--------|---------------------|------|-------------------------------------|
| POST   | /api/auth/register  | No   | Register user (+org if new slug)   |
| POST   | /api/auth/login      | No   | Login, returns access+refresh JWT  |
| POST   | /api/auth/refresh    | No   | Exchange refresh token for new pair|
| GET    | /api/health          | No   | Health check                        |
| POST   | /api/bots            | Yes  | Create a bot in your org           |
| GET    | /api/bots            | Yes  | List bots in your org              |
| GET    | /api/bots/{id}       | Yes  | Get a single bot                   |

## Schema overview

- `organizations` — tenant root
- `users` — belongs to an org, has role (owner/admin/agent)
- `bots` — belongs to an org, has `config` JSONB (will hold flow definition in Phase 3)
- `conversations` — belongs to a bot, tracks channel + session_state JSONB
- `messages` — belongs to a conversation, sender (user/bot/agent) + content

## Done-when checklist
- [ ] `docker compose up -d` runs Postgres successfully
- [ ] `alembic upgrade head` creates all tables
- [ ] Register a user via `/api/auth/register` → creates org + owner user
- [ ] Login via `/api/auth/login` → returns tokens
- [ ] Create a bot via `/api/bots` with Bearer token → persists to DB

## Deploy to Render

- **Files:** See [Dockerfile](Dockerfile) and [render.yaml](render.yaml) in the repo root.
- **Build:** Render will use the `Dockerfile` to build the image; the Dockerfile installs `backend/requirements.txt` and copies the `backend` folder into the container.
- **Port:** Render provides a `PORT` env var; the container binds to `0.0.0.0:$PORT` using `gunicorn` + `uvicorn` workers.
- **Quick steps:**

```bash
# Create a Git repo, push to GitHub (or connect your repo to Render)
git init
git add .
git commit -m "Add Dockerfile + Render config"
git push origin main

# On Render: create a new Web Service, connect your repo, select Docker, and deploy.
```

If you prefer not to use Docker, set the Start Command on Render to:

```
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
```

Make sure `backend/.env` (or Render env vars) contains your DB and JWT secrets.
