# Atlas4D Module Model

**Version:** 0.3  
**Status:** Draft  
**Last Updated:** December 2025

---

## Overview

This document defines how to extend Atlas4D with domain-specific modules without breaking the Core.

> **Philosophy:** Modules SHOULD consume Core tables, not rewrite them. Modules MAY add their own tables and views, but MUST NOT break core schema.

---

## What is a Module?

A **module** is a self-contained extension that adds domain-specific functionality to Atlas4D.

### Module Characteristics

- **Self-contained** - Own tables, services, documentation
- **Core-dependent** - Uses Core API/schema, not vice versa
- **Versioned** - Declares compatibility with Core versions
- **Optional** - Core works without any modules

---

## Module Structure
```
atlas4d-module-{name}/
├── MODULE.yaml              # Module manifest (required)
├── README.md                # Module documentation
├── sql/
│   └── schema/
│       └── 001_init.sql     # Module-specific tables
├── services/
│   └── {name}-svc/
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
├── docs/
│   ├── USAGE.md             # How to use this module
│   └── NLQ_EXAMPLES.md      # NLQ queries for this domain
├── dashboards/
│   └── grafana/
│       └── {name}_overview.json
└── seed/
    └── demo_{name}.sql      # Demo data for module
```

---

## MODULE.yaml Specification
```yaml
# MODULE.yaml - Module Manifest
name: telecom                          # MUST: Unique identifier
display_name: Atlas4D Telecom Module   # MUST: Human-readable name
version: 0.1.0                         # MUST: Semantic version
description: Network infrastructure monitoring with LSTM predictions

# Core compatibility
core:
  min_version: 0.3.0                   # MUST: Minimum Core version
  max_version: 0.3.x                   # SHOULD: Maximum tested version

# Module metadata
category: infrastructure               # telecom | mobility | airspace | security | analytics
author: Digicom Ltd
license: Apache-2.0
repository: https://github.com/crisbez/atlas4d-module-telecom

# Extension declarations
extensions:
  database:
    schema: atlas4d_telecom            # Module's schema prefix
    tables:
      - network_nodes
      - traffic_metrics
      - predictions
  
  api:
    prefix: /api/telecom               # API route prefix
    endpoints:
      - GET /nodes
      - GET /metrics
      - GET /predictions/{node_id}
  
  nlq:
    intents:
      - telecom_anomaly
      - network_status
      - traffic_forecast
    stsql_sources:
      - TELECOM_NODES
      - TELECOM_METRICS
  
  observability:
    metrics_prefix: telecom_
    dashboards:
      - telecom_overview.json

# Dependencies (other modules)
dependencies: []

# Installation hooks
hooks:
  post_install: scripts/post_install.sh
  pre_uninstall: scripts/pre_uninstall.sh
```

---

## Extension Points

### 1. Database Extension

Modules create tables in their own schema:
```sql
-- Module schema: atlas4d_{module}
CREATE SCHEMA IF NOT EXISTS atlas4d_telecom;

-- Module-specific tables
CREATE TABLE atlas4d_telecom.network_nodes (
    id              SERIAL PRIMARY KEY,
    node_type       TEXT NOT NULL,           -- olt, switch, cpe
    name            TEXT,
    location_id     BIGINT,                  -- FK to observations_core
    capacity_gbps   NUMERIC,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Views consuming Core tables
CREATE VIEW atlas4d_telecom.v_node_anomalies AS
SELECT 
    n.id AS node_id,
    n.name,
    n.node_type,
    a.anomaly_type,
    a.severity,
    a.detected_at
FROM atlas4d_telecom.network_nodes n
JOIN atlas4d.anomalies a ON a.metadata->>'node_id' = n.id::text
WHERE a.detected_at > NOW() - INTERVAL '24 hours';
```

**Rules:**
- MUST use `atlas4d_{module}` schema prefix
- MUST NOT modify Core tables directly
- MAY create views joining Core tables
- MAY add triggers on Core tables (with care)

### 2. API Extension

Modules register routes under their prefix:
```python
# services/telecom-svc/main.py
from fastapi import FastAPI, APIRouter

app = FastAPI(title="Atlas4D Telecom Module")
router = APIRouter(prefix="/api/telecom")

@router.get("/nodes")
async def list_nodes():
    """List all network nodes"""
    ...

@router.get("/nodes/{node_id}/predictions")
async def get_predictions(node_id: int, hours_ahead: int = 6):
    """Get LSTM predictions for a node"""
    ...

@router.get("/health")
async def health():
    return {"module": "telecom", "status": "healthy"}

app.include_router(router)
```

**Integration:**
- Gateway proxies `/api/telecom/*` to telecom-svc
- Module MUST implement `/health` endpoint
- Module SHOULD follow Core API conventions

### 3. NLQ Extension

Modules can add intents and STSQL sources:
```python
# Intent registration (in nlq-svc config)
TELECOM_INTENTS = {
    "telecom_anomaly": {
        "keywords": ["мрежа", "network", "OLT", "switch", "CPE", "порт", "port"],
        "handler": "telecom_anomaly_handler",
        "confidence_boost": 0.1
    },
    "network_status": {
        "keywords": ["статус", "status", "здраве", "health", "up", "down"],
        "handler": "network_status_handler"
    }
}

# STSQL source registration
TELECOM_STSQL_SOURCES = {
    "TELECOM_NODES": "atlas4d_telecom.network_nodes",
    "TELECOM_METRICS": "atlas4d_telecom.traffic_metrics"
}
```

**NLQ Examples:**
```
User: "Покажи аномалии по OLT портове"
→ Intent: telecom_anomaly
→ STSQL: SELECT * FROM TELECOM_NODES WHERE node_type = 'olt' ...

User: "Which switches had high latency yesterday?"
→ Intent: telecom_anomaly  
→ STSQL: SELECT * FROM TELECOM_METRICS WHERE metric_type = 'latency' ...
```

### 4. Observability Extension

Modules expose metrics with their prefix:
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

TELECOM_NODES_TOTAL = Gauge(
    'telecom_nodes_total',
    'Total network nodes',
    ['node_type']
)

TELECOM_ANOMALIES = Counter(
    'telecom_anomalies_total',
    'Telecom anomalies detected',
    ['anomaly_type', 'severity']
)

TELECOM_PREDICTION_LATENCY = Histogram(
    'telecom_prediction_seconds',
    'LSTM prediction latency',
    ['node_type']
)
```

**Grafana Dashboard:**
- Export as JSON to `dashboards/grafana/`
- Use variables for flexibility
- Include: node counts, anomaly rates, prediction accuracy

---

## Module Lifecycle

### Installation
```bash
# 1. Clone module
git clone https://github.com/crisbez/atlas4d-module-telecom

# 2. Run schema migration
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f atlas4d-module-telecom/sql/schema/001_init.sql

# 3. Add service to docker-compose
# (append to compose.yml or use override)

# 4. Start module service
docker compose up -d telecom-svc

# 5. Load demo data (optional)
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f atlas4d-module-telecom/seed/demo_telecom.sql
```

### Uninstallation
```bash
# 1. Stop service
docker compose stop telecom-svc

# 2. Remove schema (careful!)
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -c "DROP SCHEMA atlas4d_telecom CASCADE;"

# 3. Remove from compose
```

---

## Example Modules

### atlas4d-module-telecom (Reference)

**Purpose:** Network infrastructure monitoring

| Component | Description |
|-----------|-------------|
| Tables | network_nodes, traffic_metrics, predictions |
| Services | telecom-svc (FastAPI + LSTM) |
| NLQ | Network anomalies, traffic queries |
| Dashboard | Node health, prediction accuracy |

### atlas4d-module-airspace (Planned)

**Purpose:** Radar + ADS-B fusion, drone detection

| Component | Description |
|-----------|-------------|
| Tables | radar_tracks, adsb_positions, threats |
| Services | radar-edge, fusion-coordinator |
| NLQ | Threat queries, airspace status |
| Dashboard | Track counts, threat zones |

### atlas4d-module-vision (Planned)

**Purpose:** GPU-accelerated object detection

| Component | Description |
|-----------|-------------|
| Tables | detections, tracked_objects |
| Services | vision-svc (GPU) |
| NLQ | Object queries, detection stats |
| Dashboard | FPS, detection counts |

---

## Best Practices

### DO ✅

- Use Core tables for common data (observations, anomalies)
- Create views for complex joins
- Follow Core API conventions
- Document NLQ examples thoroughly
- Version your module semantically
- Test against declared Core versions

### DON'T ❌

- Modify Core schema directly
- Override Core API endpoints
- Create tight coupling with other modules
- Skip health endpoint implementation
- Forget observability metrics
- Break backward compatibility in minor versions

---

## Future: Module Registry

Planned for v0.5+:
```bash
# List available modules
atlas4d module list

# Check compatibility
atlas4d module check telecom

# Install module
atlas4d module install telecom

# Module info
atlas4d module info telecom
```

---

*This specification evolves with the platform. Feedback welcome via GitHub issues.*
