# Why We Built Atlas4D: The Missing 4D Data Platform

*The open-source spatiotemporal intelligence layer that PostgreSQL always needed.*

---

## The Problem: Fragmented Spatiotemporal Data

If you've ever built a system that tracks things moving through space and time, you know the pain:

- **Geographic data** lives in PostGIS
- **Time-series metrics** go to InfluxDB or TimescaleDB
- **Vector embeddings** for ML need pgvector or Pinecone
- **Real-time alerts** require yet another system

You end up with 4-5 databases, complex ETL pipelines, and queries that span multiple systems just to answer: *"What anomalies happened near the airport in the last hour?"*

We call this the **4D fragmentation problem** - where the four dimensions (latitude, longitude, altitude, time) are scattered across incompatible systems.

---

## Our Approach: One Database, Four Dimensions

Atlas4D unifies everything in PostgreSQL:
```
PostgreSQL 16
├── PostGIS      → Spatial queries, geometry, H3 hexagons
├── TimescaleDB  → Time-series, automatic partitioning
├── pgvector     → ML embeddings, semantic search
└── JSONB        → Flexible metadata, no schema migrations
```

One query language. One connection. One backup strategy.
```sql
-- Find anomalies near Sofia in the last 6 hours
SELECT * FROM atlas4d.anomalies a
JOIN atlas4d.observations_core o ON a.observation_id = o.id
WHERE o.t > NOW() - INTERVAL '6 hours'
AND ST_DWithin(o.geom, ST_MakePoint(23.32, 42.69)::geography, 10000);
```

No joins across databases. No data synchronization nightmares.

---

## Who Is Atlas4D For?

**Data Engineers** building real-time spatiotemporal pipelines who are tired of maintaining 5 different databases for one use case.

**GIS/Geo Developers** who need time-series and vector search alongside their spatial data, without leaving PostgreSQL.

**Telecom & ISP Teams** monitoring network infrastructure - OLTs, switches, CPE devices - with spatial context and anomaly detection.

**Smart City Projects** analyzing mobility patterns, traffic flow, and urban sensors in a unified platform.

**Defense & Security Organizations** tracking assets, detecting threats, and correlating events across multiple sensor types.

**Research Labs** working with trajectory data who need ML-ready embeddings and semantic search.

---

## What Makes Atlas4D Different?

### 1. Natural Language Queries (NLQ)

Ask your data in plain language:
```
"Какво е времето в Бургас?"
"Show threats near the airport"
"Покажи аномалии от последния час"
```

The NLQ engine understands Bulgarian, English, and translates to optimized STSQL queries.

### 2. Multi-Domain on One Engine

The same Atlas4D core handles:

| Domain | Data Types |
|--------|------------|
| **Mobility** | Vehicles, sensors, cameras |
| **Telecom** | OLTs, switches, CPE, traffic metrics |
| **Airspace** | Radar tracks, ADS-B, drones |
| **Agriculture** | Weather stations, soil sensors, imagery |

Switch between domains with a dropdown - the underlying 4D engine is identical.

### 3. Observability from Day One

Every Atlas4D deployment includes:

- Prometheus metrics for all services
- Grafana dashboards (NLQ latency, cache hit rates, anomaly counts)
- Structured logging with correlation IDs
- Health endpoints for every microservice

You don't bolt on monitoring later - it's built in.

### 4. ML-Ready Architecture

- **Trajectory embeddings** via sentence-transformers
- **pgvector** for similarity search
- **Anomaly scoring** with configurable thresholds
- **LSTM forecasting** for predictive alerts

---

## Atlas4D Base: The Open Core

We've open-sourced the foundation:
```bash
git clone https://github.com/crisbez/atlas4d-base
cd atlas4d-base
docker compose up -d
```

**In 5 minutes you get:**

- PostgreSQL 16 with PostGIS + TimescaleDB + pgvector
- REST API for observations, anomalies, stats
- Interactive map with real-time updates
- Demo scenarios (Mobility + Telecom)

![Atlas4D Base Demo](../quickstart/img/demo_burgas_map.png)

---

## The Full Platform

Atlas4D Base is the open core. The full Atlas4D platform adds:

| Module | Capability |
|--------|------------|
| **Radar & ADS-B** | Multi-source fusion, track correlation |
| **Network Guardian** | SNMP monitoring, LSTM predictions, topology mapping |
| **Vision GPU** | Real-time object detection, tracking |
| **Threat Forecasting** | ML-based risk scoring, predictive zones |
| **Enterprise Auth** | SSO, RBAC, audit logging |

[Contact us](mailto:office@atlas4d.tech) for enterprise inquiries.

---

## Why PostgreSQL?

We bet on PostgreSQL because:

1. **It's everywhere** - Your team already knows it
2. **Extensions are powerful** - PostGIS, TimescaleDB, pgvector are production-grade
3. **One operational model** - Backup, replication, monitoring - all standard
4. **SQL is universal** - No proprietary query language to learn

The "boring technology" choice that lets us focus on the 4D intelligence layer, not database operations.

---

## Try It Now
```bash
# Clone
git clone https://github.com/crisbez/atlas4d-base

# Start
cd atlas4d-base && docker compose up -d

# Load demo data
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f /docker-entrypoint-initdb.d/seed/demo_burgas.sql

# Open the map
open http://localhost:8091
```

**Time to first map: ~5 minutes**

---

## What's Next?

We're building Atlas4D to be the "Linux of 4D spatiotemporal platforms" - a solid open foundation that organizations can extend for their specific domains.

Upcoming:

- [ ] Kubernetes Helm charts
- [ ] RAG integration for document-aware queries
- [ ] Real-time WebSocket streaming
- [ ] Multi-tenant SaaS deployment

Star us on [GitHub](https://github.com/crisbez/atlas4d-base) and join the journey.

---

*Atlas4D is built by [Digicom Ltd](https://digicom.bg), a technology company based in Bulgaria focused on spatiotemporal intelligence and network analytics.*

---

**Tags:** #postgresql #spatiotemporal #timeseries #gis #postgis #timescaledb #pgvector #opensource #4d #realtime #anomalydetection
