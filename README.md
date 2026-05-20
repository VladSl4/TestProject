# Vibe Tasks

A "vibe-driven" todo prototype. Three Python microservices communicate over
gRPC; a Next.js + Tailwind frontend talks REST to the gateway.

---

## Architecture

```
┌──────────────┐   REST    ┌──────────────────┐   gRPC   ┌──────────────────┐   gRPC   ┌──────────────────┐
│   Frontend   │ ────────► │     gateway      │ ───────► │  proxy_service   │ ───────► │ database_service │
│ Next.js :3000│           │    REST :8000    │          │    gRPC :5002    │          │ gRPC :5001+SQLite│
└──────────────┘           └──────────────────┘          └──────────────────┘          └──────────────────┘
                            • CORS                       • Cross-cutting             • Owns the schema
                            • Public REST API              concerns (caching,        • Repository over
                            • Vibe Check logic             retries, fan-out)           SQLite
                            • Typed gRPC client          • gRPC server impl
```

Only the gateway speaks REST. The two inner services talk to each other
entirely over gRPC.

### Project layout

```
backend/
├── rpc/
│   ├── protos/                       # Centralized .proto contracts
│   │   ├── database_service/database_tasks.proto
│   │   └── proxy_service/proxy_tasks.proto
│   ├── generated/                    # Auto-generated Python stubs (gitignored)
│   └── gen_protos.py                 # protoc wrapper
│
├── database_service/
│   ├── interfaces/                   # AbstractTasksRepository, AbstractTasksService
│   ├── models/                       # VibeTask, VibeStatus
│   ├── repositories/                 # SQLite-backed implementation
│   ├── services/
│   │   ├── tasks_service.py          # Business logic
│   │   └── grpc/                     # gRPC server-side implementations
│   ├── mapping/                      # proto <-> domain
│   ├── config.py
│   ├── container.py                  # Dependency wiring
│   ├── main.py                       # Entry point
│   └── requirements.txt
│
├── proxy_service/
│   ├── interfaces/                   # AbstractProxyTasksService
│   ├── services/
│   │   ├── proxy_tasks_service.py    # Forwards to database_service over gRPC
│   │   └── grpc/                     # gRPC server-side implementation
│   ├── mapping/                      # proto <-> proto across the two services
│   ├── config.py
│   ├── container.py                  # Builds the outbound gRPC client + service
│   ├── main.py
│   └── requirements.txt
│
├── gateway/
│   ├── interfaces/                   # AbstractVibeService
│   ├── controllers/                  # FastAPI REST routers
│   ├── services/                     # VibeService (uses proxy gRPC client)
│   ├── mapping/                      # proto <-> public DTO
│   ├── models/                       # Pydantic DTOs for the REST API
│   ├── config.py
│   ├── dependencies.py               # FastAPI DI providers
│   ├── main.py
│   └── requirements.txt
│
└── tests/
    └── database_service/
        ├── test_tasks_repository.py
        ├── test_tasks_service.py
        └── grpc/
            └── test_tasks_data_service.py
```

---

## Tech stack

- **Backend:** Python 3.12+, FastAPI 0.115 (gateway only), Pydantic 2,
  grpcio 1.66, protobuf 5.28, SQLite (stdlib `sqlite3`)
- **Frontend:** Next.js 14 (App Router), React 18, TypeScript 5, Tailwind CSS 3
- **Tests:** pytest (backend, including in-process gRPC servicer tests);
  Vitest + Testing Library + Playwright (frontend)

---

## Getting started

### 1. Install backend + generate gRPC stubs

```powershell
.\install_backend.ps1
```

That runs:
1. `pip install -r backend/requirements.txt`
2. `python backend/rpc/gen_protos.py` — compiles every `.proto` into
   `backend/rpc/generated/<service>/{*_pb2.py, *_pb2_grpc.py, *_pb2.pyi}`.

Re-run `python backend/rpc/gen_protos.py` after editing any `.proto`.

### 2. Install + run the frontend

```powershell
cd frontend
npm install
copy .env.local.example .env.local   # NEXT_PUBLIC_API_BASE_URL -> http://127.0.0.1:8000
npm run dev
```

Open http://localhost:3000.

### 3. Run the backend (three windows)

```powershell
.\start_backend.ps1
```

Spins up:
- `database_service` — gRPC at `127.0.0.1:5001`
- `proxy_service`    — gRPC at `127.0.0.1:5002` (calls database_service)
- `gateway`          — REST at `http://127.0.0.1:8000/docs` (calls proxy_service)

Or run them manually from `backend/`:

```powershell
py -3 -m database_service.main
py -3 -m proxy_service.main
py -3 -m gateway.main
```

---

## Features

- **CRUD** for Vibe Tasks (create, list, status transition, delete).
- **Vibe Check button** — `POST /api/tasks/{id}/vibe-check` (gateway) picks a
  random mood emoji + caption from a curated palette and writes the emoji
  onto the task through the proxy -> database gRPC pipeline.
- **Optimistic UI** — create/update/delete reconcile from server responses.
- **Three columns** — Pending -> In-Progress -> Groovy.

---

## Tests

### Backend (pytest)

```powershell
cd backend
py -3 -m pytest
```

Covers:

1. `tests/database_service/test_tasks_repository.py` — 4 repository CRUD tests
   against a real (temp) SQLite file.
2. `tests/database_service/test_tasks_service.py` — 3 business-service tests.
3. `tests/database_service/grpc/test_tasks_data_service.py` — gRPC server-side
   test of the task-creation RPC.

> The gRPC tests need the generated stubs. If you skipped step 1 of install,
> run `python backend/rpc/gen_protos.py` first or those tests will be skipped.

### Frontend

```powershell
cd frontend
npm test                  # Vitest — list rendering
npm run test:e2e          # Playwright — task creation flow
```

---

## Public API (gateway, REST, port 8000)

| Method | Path                              | Purpose                                    |
|--------|-----------------------------------|--------------------------------------------|
| GET    | `/api/tasks`                      | List all Vibe Tasks                        |
| GET    | `/api/tasks/{id}`                 | Get a single Vibe Task                     |
| POST   | `/api/tasks`                      | Create a task `{ title, description? }`    |
| PATCH  | `/api/tasks/{id}`                 | Update title/description/status/mood_emoji |
| DELETE | `/api/tasks/{id}`                 | Delete a task                              |
| POST   | `/api/tasks/{id}/vibe-check`      | Run mock vibe analysis — returns a mood    |
| GET    | `/health`                         | Liveness probe                             |

`VibeStatus` values exposed by REST: `"Pending" | "InProgress" | "Groovy"`.

### Internal gRPC surface

```
database_service -> service vibetasks.database.RpcTasksDataService  { ListTasks, GetTask, CreateTask, UpdateTask, DeleteTask }
proxy_service    -> service vibetasks.proxy.RpcTasksProxyService    { ListTasks, GetTask, CreateTask, UpdateTask, DeleteTask }
```

Browse the contracts under `backend/rpc/protos/`.

---

## Notes

- SQLite file lives at `backend/vibe_tasks.db` (auto-created on first run).
  Override with `DATABASE_SERVICE_DB_PATH`.
- Inter-service addresses are env-driven (`DATABASE_SERVICE_ADDRESS`,
  `PROXY_SERVICE_ADDRESS`, `GATEWAY_CORS_ORIGINS`). Defaults assume localhost.
