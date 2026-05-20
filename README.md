# VibeLog — AI-Powered Log Analyzer

DevOps engineers paste raw text logs, hit **Generate Insights**, and the
backend returns a distilled JSON summary with a category and recommended
action.

Three Python microservices communicate over gRPC; a Next.js + Tailwind
frontend talks REST to the gateway.

---

## Architecture

```
┌──────────────┐   REST    ┌──────────────────┐   gRPC   ┌──────────────────┐   gRPC   ┌──────────────────┐
│   Frontend   │ ────────► │     gateway      │ ───────► │  proxy_service   │ ───────► │ database_service │
│ Next.js :3000│           │    REST :8000    │          │    gRPC :5002    │          │ gRPC :5001+SQLite│
└──────────────┘           └──────────────────┘          └──────────────────┘          └──────────────────┘
                            • CORS                       • Analyzer (AI sim)        • Owns the schema
                            • Public REST API            • Persists results         • Persists analysis
                            • Pure HTTP↔gRPC bridge        through database tier      history
                            • Typed gRPC client          • gRPC server impl
```

Only the gateway speaks REST. The two inner services talk to each other
entirely over gRPC. The gateway holds **zero business logic** — it just
forwards requests to proxy_service and maps the proto response back to
the public REST DTO.

### How the analyzer works

The `AnalyzerService` (in `backend/proxy_service/services/analyzer_service.py`)
simulates an LLM call:

1. Sleeps for `PROXY_ANALYZER_LATENCY_SECONDS` (default **1.0 s**, the
   target from the brief).
2. Splits the raw logs into lines and keyword-matches them against
   `error|exception|fatal|critical|panic|traceback|failed|failure` and
   `warn|warning|deprecated`.
3. Classifies as **Error** > **Warning** > **Info** (error wins).
4. Returns `{ summary, category, recommended_action }`. The proxy's
   `Analyze` RPC immediately persists the result via database_service.

To swap in a real LLM (OpenAI/Anthropic), replace the body of
`AnalyzerService.analyze` — the interface stays the same.

### Project layout

```
backend/
├── rpc/
│   ├── protos/
│   │   ├── database_service/database_analyses.proto    # RpcLogsAnalysisService
│   │   └── proxy_service/proxy_analyses.proto          # RpcLogsProxyService
│   ├── generated/                                      # Auto-generated stubs (gitignored)
│   └── gen_protos.py
│
├── database_service/      # SQLite-backed CRUD over analyses
├── proxy_service/         # Analyzer (AI sim) + forwards to database via gRPC
├── gateway/               # Public REST API (pure HTTP↔gRPC bridge, no logic)
└── tests/
    ├── database_service/test_analyses_repository.py
    └── proxy_service/test_analyzer_service.py

frontend/
├── app/                   # Next.js App Router
├── components/
│   ├── LogAnalyzer.tsx    # Main dashboard (textarea + history)
│   ├── InsightCard.tsx
│   ├── CategoryBadge.tsx
│   └── HistoryList.tsx
├── lib/
│   ├── api.ts             # fetch wrappers
│   └── types.ts
└── tests/
    └── LogAnalyzer.test.tsx  # Integration test (mocked fetch)
```

---

## Tech stack

- **Backend:** Python 3.12+ (tested on 3.14), FastAPI, Pydantic 2, grpcio,
  protobuf, SQLite (stdlib `sqlite3`)
- **Frontend:** Next.js 14 (App Router), React 18, TypeScript 5,
  Tailwind CSS 3
- **Tests:** pytest (backend); Vitest + Testing Library (frontend)

---

## Getting started

### 1. Install backend + generate gRPC stubs

```powershell
.\install_backend.ps1
```

That runs:
1. `pip install -r backend/requirements.txt`
2. `python backend/rpc/gen_protos.py` — compiles every `.proto` into
   `backend/rpc/generated/<service>/`.

Re-run `python backend/rpc/gen_protos.py` after editing any `.proto`.

### 2. Install + run the frontend

```powershell
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**.

The frontend defaults to `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`.
Set it in `.env.local` if your gateway is elsewhere.

### 3. Run the backend (three windows)

```powershell
.\start_backend.ps1
```

Spins up:
- `database_service` — gRPC at `127.0.0.1:5001`
- `proxy_service`    — gRPC at `127.0.0.1:5002`
- `gateway`          — REST at `http://127.0.0.1:8000/docs`

Or run them manually from `backend/` (in three separate shells):

```powershell
py -3 -m database_service.main
py -3 -m proxy_service.main
py -3 -m gateway.main
```

---

## Tests

### Backend (pytest)

```powershell
cd backend
py -3 -m pytest
```

Covers (8 tests):
- `tests/proxy_service/test_analyzer_service.py` — analyzer logic (empty
  input, info-only, warning detection, error-wins-over-warning, latency).
- `tests/database_service/test_analyses_repository.py` — repository CRUD
  against a temp SQLite file.

### Frontend (Vitest + Testing Library)

```powershell
cd frontend
npm test
```

Integration test in `tests/LogAnalyzer.test.tsx` mocks `fetch` and
verifies:
- The dashboard renders the backend insight (summary + recommended action
  + category badge) after Generate Insights is clicked.
- A failed API call surfaces an error banner instead of an insight.
- The button is disabled while the analysis is in flight.

---

## Public API (gateway, REST, port 8000)

```
POST   /api/analyze            Body { raw_logs } -> { id, summary, category, recommended_action, created_at }
GET    /api/analyses           Recent analyses (newest first) for the history pane
DELETE /api/analyses/{id}      Remove a history entry
GET    /health                 Liveness probe
```

`category` values: `"Info" | "Warning" | "Error"`.

### Internal gRPC surface

```
database_service -> service vibelog.database.RpcLogsAnalysisService  { List, Get, Save, Delete }
proxy_service    -> service vibelog.proxy.RpcLogsProxyService        { Analyze, List, Get, Delete }
```

Browse the contracts under `backend/rpc/protos/`.

---

## UX behaviour

- **Loading state** — while the analyzer runs (≥ 1 s), the button is
  disabled, the textarea is read-only, and a `"Talking to the AI…"`
  pulse appears.
- **Error state** — if the gateway returns non-2xx (or the network
  fails), the dashboard shows a dismissable red banner with the API
  error message.
- **Acceptance latency** — 1 s analyzer delay + sub-100 ms gRPC + sub-50 ms
  React render = well under the 5 s budget from the brief.

---

## Notes

- SQLite file lives at `backend/vibelog.db` (auto-created on first run).
  Override with `DATABASE_SERVICE_DB_PATH`.
- Inter-service addresses are env-driven (`DATABASE_SERVICE_ADDRESS`,
  `PROXY_SERVICE_ADDRESS`, `GATEWAY_CORS_ORIGINS`,
  `PROXY_ANALYZER_LATENCY_SECONDS`). Defaults assume localhost.
- Setting `PROXY_ANALYZER_LATENCY_SECONDS=0` removes the simulated
  delay (useful in CI).
