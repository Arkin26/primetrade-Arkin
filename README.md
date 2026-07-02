Live: https://primetrade-arkin.vercel.app/
Credentials: admin@example.com, PSWRD = change-me


# Primetrade

Primetrade is a full stack task management application built as a scalable REST API with authentication, role based access control, and a React frontend for testing and demo.

Anyone can register an account, sign in, and manage their own tasks. Admins can view all tasks and manage users. The backend is versioned, documented, and covered by automated tests.

## What this project includes

<b>Backend (FastAPI)</b>
- User registration and login with password hashing and JWT tokens
- Role based access: regular users and admins
- Full CRUD for tasks
- API versioning under `/api/v1`
- Input validation and consistent error responses
- PostgreSQL database with Alembic migrations
- Swagger docs, Postman collection, and pytest test suite
- Docker Compose setup for local development

<b>Frontend (React + Vite)</b>
- Register and sign in pages
- Protected dashboard (requires a valid JWT)
- Create, edit, delete, and filter tasks
- Success and error messages from API responses
- Admin panel to list users and change roles (admin only)

## Tech stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.11+ |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React, TypeScript, Vite |
| Testing | pytest (backend) |
| Deployment | Docker, Docker Compose |

## Admin credentials

Use these to sign in as an admin and access the admin panel:

<b>Email:</b> admin@example.com  
<b>Password:</b> change-me

These come from the `.env` file (`ADMIN_EMAIL` and `ADMIN_PASSWORD`). Change them in `.env` before deploying to production.

## Quick start

### 1. Start the backend (Docker)

```bash
cp .env.example .env
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

<b>Postgres port note:</b> Docker exposes PostgreSQL on host port 5433 (not 5432) to avoid conflicts if you already have Postgres running locally.

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

| Service | URL |
|---------|-----|
| Web UI | http://localhost:5173 |

Make sure the API is running and `CORS_ORIGINS` in `.env` includes `http://localhost:5173`.

### 3. Try it out

1. Open http://localhost:5173
2. Sign in with the admin credentials above, or register a new user
3. Create and manage tasks on the dashboard
4. As admin, open the Admin tab to view users and change roles

## Project structure

```
primetrade/
├── app/                 # FastAPI backend
│   ├── api/v1/          # Versioned API routes
│   ├── core/            # Config, security, dependencies
│   ├── db/              # Models and database session
│   ├── schemas/         # Pydantic request/response models
│   └── services/        # Business logic
├── alembic/             # Database migrations
├── tests/               # Backend pytest suite
├── frontend/            # React UI
├── postman/             # Postman API collection
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API overview

Base path: `/api/v1`

| Method | Path | Access | Description |
|--------|------|--------|-------------|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and receive JWT |
| GET | `/auth/me` | JWT | Current user profile |
| GET | `/tasks` | JWT | List tasks (paginated) |
| POST | `/tasks` | JWT | Create a task |
| GET | `/tasks/{id}` | JWT | Get one task |
| PATCH | `/tasks/{id}` | JWT | Update a task |
| DELETE | `/tasks/{id}` | JWT | Delete a task |
| GET | `/users` | Admin | List all users |
| PATCH | `/users/{id}/role` | Admin | Update a user's role |
| GET | `/health` | Public | Liveness check |
| GET | `/health/ready` | Public | Database readiness check |

<b>Task ownership rules</b>
- Regular users can only view and manage their own tasks
- Admins can view and manage all tasks

## Local backend development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

You need a running PostgreSQL instance. Update `DATABASE_URL` in `.env` to match your setup.

## Running tests

<b>Backend</b>

```bash
pytest -v
```

## API documentation and Postman

- Interactive docs: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
- Postman collection: import `postman/primetrade-api.json` and set `base_url` to `http://localhost:8000`

## Error response format

All API errors return a consistent JSON shape:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found",
    "details": null
  }
}
```

## Environment variables

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | PostgreSQL connection string |
| JWT_SECRET | Secret key for signing tokens |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiry time |
| CORS_ORIGINS | Allowed frontend origins |
| ADMIN_EMAIL | Default admin email (seeded on startup) |
| ADMIN_PASSWORD | Default admin password (seeded on startup) |

## License

Built for educational and assignment purposes.
# primetrade-Arkin
