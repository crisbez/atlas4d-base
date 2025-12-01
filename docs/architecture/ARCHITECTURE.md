# Atlas4D Architecture Overview

## Design Principles

1. **PostgreSQL as the Core** - All spatiotemporal data in one database
2. **Microservices for Scale** - Independent services for different concerns
3. **Observability First** - Metrics, logs, and traces from day one
4. **Developer Experience** - Quick start, clear APIs, good docs

## System Architecture
```
                                    ┌─────────────────┐
                                    │   Web Browser   │
                                    └────────┬────────┘
                                             │
                                    ┌────────▼────────┐
                                    │     Nginx       │
                                    │   (Frontend)    │
                                    └────────┬────────┘
                                             │
┌────────────────────────────────────────────▼─────────────────────────────────────┐
│                              API Gateway (FastAPI)                                │
│  • Authentication (JWT)                                                          │
│  • Rate limiting                                                                 │
│  • Request routing                                                               │
│  • Circuit breakers                                                              │
└──────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┘
       │              │              │              │              │
┌──────▼─────┐ ┌──────▼─────┐ ┌──────▼─────┐ ┌──────▼─────┐ ┌──────▼─────┐
│ Public API │ │ Anomaly Svc│ │Threat Fore-│ │ Embedding  │ │  NLQ Svc   │
│            │ │            │ │  castor    │ │    Svc     │ │            │
│ • Ingest   │ │ • Detect   │ │ • Score    │ │ • Vectors  │ │ • Parse    │
│ • Query    │ │ • Fuse     │ │ • Forecast │ │ • Cache    │ │ • Execute  │
│ • Stats    │ │ • Alert    │ │ • Zones    │ │ • Search   │ │ • Format   │
└──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
       │              │              │              │              │
       └──────────────┴──────────────┴──────┬───────┴──────────────┘
                                            │
                              ┌─────────────▼─────────────┐
                              │          Redis            │
                              │  • Intent cache           │
                              │  • Embedding cache        │
                              │  • Session store          │
                              └─────────────┬─────────────┘
                                            │
                              ┌─────────────▼─────────────┐
                              │        PostgreSQL         │
                              │  ┌─────────────────────┐  │
                              │  │      PostGIS        │  │
                              │  │  (Spatial queries)  │  │
                              │  └─────────────────────┘  │
                              │  ┌─────────────────────┐  │
                              │  │    TimescaleDB      │  │
                              │  │  (Time-series)      │  │
                              │  └─────────────────────┘  │
                              │  ┌─────────────────────┐  │
                              │  │        H3           │  │
                              │  │  (Hex indexing)     │  │
                              │  └─────────────────────┘  │
                              │  ┌─────────────────────┐  │
                              │  │     pgvector        │  │
                              │  │  (Vector search)    │  │
                              │  └─────────────────────┘  │
                              └───────────────────────────┘
```

## Data Flow

### 1. Ingestion Flow
```
External Source → Public API → Validation → PostgreSQL
                                    ↓
                              H3 Indexing
                                    ↓
                              TimescaleDB (time partitioning)
```

### 2. Anomaly Detection Flow
```
New Observation → Anomaly Service → Statistical Analysis
                                           ↓
                                    Fusion Service
                                           ↓
                                    Threat Forecastor
                                           ↓
                                    Risk Score + Zone
```

### 3. Query Flow (NLQ)
```
User Query → NLQ Service → Intent Detection (Redis cache)
                                    ↓
                           LLM Translation (if needed)
                                    ↓
                           SQL Generation
                                    ↓
                           PostgreSQL Query
                                    ↓
                           Response Formatting
```

## Database Schema (Simplified)
```sql
-- Core observation table (TimescaleDB hypertable)
atlas4d.observations_core (
    id          BIGSERIAL,
    t           TIMESTAMPTZ,      -- Time
    geom        GEOMETRY(Point),  -- Location (PostGIS)
    h3_index    H3INDEX,          -- H3 cell
    source_type VARCHAR,
    track_id    UUID,
    lat, lon    FLOAT,
    metadata    JSONB
)

-- Trajectory embeddings (pgvector)
atlas4d.trajectory_embeddings (
    id          SERIAL,
    track_id    UUID,
    embedding   VECTOR(768),      -- pgvector
    created_at  TIMESTAMPTZ
)

-- Anomalies
atlas4d.anomalies (
    id          SERIAL,
    observation_id BIGINT,
    anomaly_type VARCHAR,
    severity    INTEGER,
    detected_at TIMESTAMPTZ
)
```

## Service Ports (Default)

| Service | Internal Port | External Port |
|---------|--------------|---------------|
| API Gateway | 8000 | 8080 |
| Public API | 8000 | - |
| Anomaly Svc | 8000 | - |
| Threat Forecastor | 8000 | - |
| Embedding Svc | 8015 | - |
| NLQ Svc | 8001 | - |
| PostgreSQL | 5432 | 5432 |
| Redis | 6379 | 6379 |

## Observability Stack
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Prometheus  │────▶│   Grafana   │────▶│   Alerts    │
│  (Metrics)  │     │ (Dashboards)│     │  (Slack)    │
└─────────────┘     └─────────────┘     └─────────────┘
       ▲
       │ /metrics
       │
┌──────┴──────┐
│ All Services│
└─────────────┘
```

## Security

- JWT authentication for API access
- Rate limiting per client
- Input validation on all endpoints
- No credentials in code (environment variables)

## Scaling Considerations

- PostgreSQL: Read replicas for query scaling
- Services: Horizontal scaling via container orchestration
- Redis: Cluster mode for high availability
- TimescaleDB: Automatic partitioning handles time-series growth
