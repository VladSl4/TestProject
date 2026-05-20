# rpc

Centralized gRPC contracts shared by all backend services.

```
rpc/
├── protos/
│   ├── database_service/
│   │   └── database_analyses.proto    # RpcLogsAnalysisService
│   └── proxy_service/
│       └── proxy_analyses.proto       # RpcLogsProxyService
├── generated/                         # Auto-generated Python stubs (gitignored)
└── gen_protos.py                      # protoc wrapper
```

Run `python backend/rpc/gen_protos.py` after editing any `.proto`.
