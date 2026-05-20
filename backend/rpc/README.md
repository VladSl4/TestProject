# rpc

Centralized gRPC contracts shared by all backend services.

```
rpc/
├── protos/
│   ├── database_service/
│   │   └── database_tasks.proto    # RpcTasksDataService (DB-level CRUD)
│   └── proxy_service/
│       └── proxy_tasks.proto       # RpcTasksProxyService (mid-tier)
├── generated/                      # Auto-generated Python stubs (gitignored)
└── gen_protos.py                   # protoc wrapper
```

Run `python backend/rpc/gen_protos.py` after editing any `.proto`.
Generated stubs land under `rpc/generated/<service>/` and are added to
`sys.path` by each service's `main.py`.
