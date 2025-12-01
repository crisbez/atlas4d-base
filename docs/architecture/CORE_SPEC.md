# Atlas4D Core Specification

**Version:** 0.3  
**Status:** Evolving (migrations provided for breaking changes)  
**Last Updated:** December 2025

---

## Overview

This document defines what constitutes "Atlas4D Core" - the stable contract that users and module developers can rely upon.

> **Philosophy:** Core v0.3 is still allowed to evolve, but we commit to keeping it stable and providing migrations for any breaking changes.

---

## Core Contract Language

- **MUST** - Required for Core compliance
- **SHOULD** - Recommended, deviation needs justification
- **MAY** - Optional, at implementer's discretion

---

## 1. Database Core

### 1.1 Required Extensions

Atlas4D Core **MUST** include these PostgreSQL extensions:

| Extension | Purpose | Version |
|-----------|---------|---------|
| PostGIS | Spatial queries, geometry | 3.4+ |
| TimescaleDB | Time-series partitioning | 2.x |
| pgvector | ML embeddings, similarity search | 0.5+ |
| H3 | Hexagonal spatial indexing | Available via PostGIS |

### 1.2 Core Schema: `atlas4d.*`

**Public Contract Tables** (stable, backward compatible):

| Table | Purpose | Stability |
|-------|---------|-----------|
| `observations_core` | Main spatiotemporal data (hypertable) | **Stable** |
| `anomalies` | Detected anomalies with severity | **Stable** |
| `trajectory_embeddings` | ML trajectory vectors | **Stable** |
| `nlq_sessions` | NLQ conversation sessions | **Stable** |
| `nlq_messages` | NLQ conversation history | **Stable** |

**Internal Tables** (may change without notice):

| Table | Purpose |
|-------|---------|
| `_internal_*` | Internal processing state |
| `_cache_*` | Temporary cache tables |

### 1.3 Core Schema Contract
```sql
-- observations_core: Public Contract
CREATE TABLE atlas4d.observations_core (
    id              BIGSERIAL,
    t               TIMESTAMPTZ NOT NULL,      -- MUST: Time (partition key)
    geom            GEOMETRY(Point, 4326),     -- MUST: Location
    source_type     TEXT,                      -- MUST: Data source identifier
    track_id        UUID,                      -- SHOULD: For trajectory grouping
    entity_id       UUID,                      -- MAY: Entity identifier
    lat             DOUBLE PRECISION,          -- MUST: Convenience latitude
    lon             DOUBLE PRECISION,          -- MUST: Convenience longitude
    altitude_m      DOUBLE PRECISION,          -- MAY: Altitude
    speed_ms        DOUBLE PRECISION,          -- MAY: Speed
    heading_deg     DOUBLE PRECISION,          -- MAY: Heading
    metadata        JSONB DEFAULT '{}',        -- MUST: Flexible attributes
    PRIMARY KEY (id, t)
);

-- anomalies: Public Contract
CREATE TABLE atlas4d.anomalies (
    id              SERIAL PRIMARY KEY,
    observation_id  BIGINT,                    -- SHOULD: Link to observation
    anomaly_type    TEXT,                      -- MUST: Type identifier
    severity        INTEGER CHECK (1-5),       -- MUST: 1=low, 5=critical
    score           DOUBLE PRECISION,          -- MUST: Confidence 0.0-1.0
    detected_at     TIMESTAMPTZ DEFAULT NOW(), -- MUST: Detection time
    metadata        JSONB DEFAULT '{}'         -- MUST: Additional context
);
```

### 1.4 Guaranteed Indexes

Core **MUST** provide these indexes:
```sql
-- Spatial queries
CREATE INDEX idx_obs_geom ON observations_core USING GIST (geom);

-- Source filtering
CREATE INDEX idx_obs_source ON observations_core (source_type);

-- Trajectory queries
CREATE INDEX idx_obs_track ON observations_core (track_id);
```

---

## 2. API Core

### 2.1 Required Endpoints

Core **MUST** expose these endpoints (backward compatible):

| Endpoint | Method | Purpose | Stability |
|----------|--------|---------|-----------|
| `/health` | GET | Service health check | **Stable** |
| `/api/stats` | GET | Platform statistics | **Stable** |
| `/api/observations` | GET | Query observations | **Stable** |
| `/api/observations` | POST | Create observation | **Stable** |
| `/api/anomalies` | GET | Query anomalies | **Stable** |
| `/api/geojson/observations` | GET | Map-ready GeoJSON | **Stable** |

### 2.2 Health Response Contract
```json
{
  "status": "healthy|degraded|unhealthy",
  "postgres": "healthy|unhealthy",
  "redis": "healthy|unhealthy|not connected",
  "version": "1.0.0"
}
```

### 2.3 Observations Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lat` | float | - | Center latitude |
| `lon` | float | - | Center longitude |
| `radius_km` | float | 10 | Search radius |
| `hours` | int | 24 | Time window |
| `limit` | int | 100 | Max results |
| `source_type` | string | - | Filter by source |

### 2.4 Response Format

All API responses **MUST** be JSON. List endpoints return arrays. Error responses:
```json
{
  "detail": "Error description",
  "status_code": 400
}
```

---

## 3. NLQ Core

### 3.1 Supported Languages

| Language | Status | Examples |
|----------|--------|----------|
| Bulgarian | **Full support** | "Какво е времето в Бургас?" |
| English | **Full support** | "Show threats near Sofia" |
| German | Basic | "Zeige Anomalien" |
| Spanish | Basic | "Mostrar anomalías" |

### 3.2 Guaranteed Query Domains

Core NLQ **MUST** understand these domains:

| Domain | Keywords | Example |
|--------|----------|---------|
| Weather | времето, temperature, forecast | "Какво е времето в София?" |
| Threats | заплахи, threats, danger | "Show threats near airport" |
| Anomalies | аномалии, anomalies, unusual | "Покажи аномалии днес" |
| Observations | покажи, show, find | "Find vehicles in Burgas" |

### 3.3 Session Memory

NLQ Core **SHOULD** support conversation context:

- Multi-turn queries: "А в София?" (after asking about Burgas)
- Session persistence via `session_id`
- Context window: last 5 messages

### 3.4 Response Format
```json
{
  "success": true,
  "query_type": "weather_fast|multi_source_fusion|...",
  "language": "bg|en",
  "explanation": "Human-readable result",
  "entities_found": [...],
  "confidence": 0.95,
  "session_id": "uuid"
}
```

---

## 4. Observability Core

### 4.1 Prometheus Metrics

Core services **MUST** expose `/metrics` with:

| Metric | Type | Description |
|--------|------|-------------|
| `{service}_requests_total` | Counter | Total requests |
| `{service}_request_duration_seconds` | Histogram | Latency |
| `{service}_errors_total` | Counter | Error count |

NLQ service **SHOULD** additionally expose:

| Metric | Type | Description |
|--------|------|-------------|
| `nlq_cache_hits_total` | Counter | Cache hits |
| `nlq_cache_misses_total` | Counter | Cache misses |
| `nlq_llm_duration_seconds` | Histogram | LLM call latency |

### 4.2 Health Checks

All Core services **MUST** implement:

- HTTP health endpoint (`/health`)
- Docker HEALTHCHECK instruction
- Graceful degradation (continue if optional deps fail)

### 4.3 Logging

Core services **SHOULD**:

- Use structured logging (JSON)
- Include correlation IDs for tracing
- Log at INFO level by default

---

## 5. What is NOT Core

The following are **experimental** or **module-specific**:

| Component | Status | Notes |
|-----------|--------|-------|
| Radar integration | Module | atlas4d-module-airspace |
| Network Guardian | Module | atlas4d-module-telecom |
| Vision/GPU detection | Module | atlas4d-module-vision |
| LSTM predictions | Experimental | May change API |
| RAG integration | Planned | Not yet stable |

Modules **MAY** depend on Core, but Core **MUST NOT** depend on modules.

---

## 6. Versioning Policy

### 6.1 Version Format
```
Atlas4D Core v{major}.{minor}.{patch}

major: Breaking changes to Core contract
minor: New features, backward compatible
patch: Bug fixes only
```

### 6.2 Current Version
```
Atlas4D Core v0.3.0
├── Schema: v0.3
├── API: v0.3
└── NLQ: v0.3
```

### 6.3 Breaking Change Policy

When Core contract changes:

1. Announce in CHANGELOG.md
2. Provide migration guide
3. Deprecation period: 1 minor version
4. Remove in next major version

---

## 7. Compliance Checklist

A deployment is "Atlas4D Core Compliant" if:

- [ ] PostgreSQL 16+ with required extensions
- [ ] Core schema tables exist with required columns
- [ ] Core API endpoints respond correctly
- [ ] Health endpoint returns valid response
- [ ] Metrics endpoint exposes required metrics

---

*This specification evolves with the platform. See CHANGELOG.md for history.*
