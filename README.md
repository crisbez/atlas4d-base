# 🌐 Atlas4D Base

**Open 4D Spatiotemporal AI Platform built on PostgreSQL**

Atlas4D Base is the **open-core** of the larger Atlas4D platform. This repo contains a minimal but fully working 4D stack - database, core services, and observability. The full Atlas4D platform adds extra domain modules (radar, drones, telco network analytics, etc.).

## ✨ What Makes Atlas4D Different

| Feature | Traditional Approach | Atlas4D |
|---------|---------------------|---------|
| **Data Model** | Separate geo, time, vector DBs | Unified PostgreSQL stack |
| **Spatial Indexing** | R-tree only | H3 hexagons + PostGIS |
| **Time Series** | Separate TSDB | TimescaleDB integrated |
| **Vector Search** | External service | pgvector in-database |
| **ML Pipeline** | Build from scratch | Ready anomaly/threat detection |
| **Natural Language** | Not included | NLQ query interface |
| **Observability** | DIY | Prometheus + Grafana + Alerts |

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/crisbez/atlas4d-base.git
cd atlas4d-base

# Start the platform
docker compose up -d

# Open the map UI (port may vary, see docs/quickstart/QUICK_START.md)
# Open in your browser: http://localhost:8091
```

**Time to first map: ~5 minutes**

## 🧱 Modular by Design

Atlas4D is built as a set of independent services around a shared 4D database core.

- **Add new domain modules** without touching the core DB
- **Mix & match services** (anomaly only, or anomaly + threat + NLQ)
- **Safe to extend:** everything talks HTTP/JSON or SQL
- **Scalable:** suitable for single-node labs and multi-service production clusters

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Atlas4D Platform                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │   Map   │  │   NLQ   │  │ Health  │  │  API    │  UI    │
│  │   UI    │  │  Chat   │  │Dashboard│  │  Docs   │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
│  ┌────┴────────────┴────────────┴────────────┴────┐        │
│  │              API Gateway (FastAPI)              │        │
│  └────┬────────────┬────────────┬────────────┬────┘        │
│       │            │            │            │              │
│  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐  ┌────┴────┐        │
│  │ Anomaly │  │ Threat  │  │Embedding│  │ Public  │Services│
│  │   Svc   │  │Forecast │  │   Svc   │  │   API   │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
│  ┌────┴────────────┴────────────┴────────────┴────┐        │
│  │     PostgreSQL + PostGIS + TimescaleDB          │  Data  │
│  │              + H3 + pgvector                    │  Layer │
│  └─────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Core Components

### Database Layer
- **PostgreSQL 16** - Rock-solid foundation
- **PostGIS 3.4** - Spatial operations and geometry
- **TimescaleDB** - Time-series hypertables with compression
- **H3** - Uber's hexagonal hierarchical indexing
- **pgvector** - Vector similarity search for embeddings

### Services (Reference Implementation)
- **public-api** - REST API for data ingestion and queries
- **anomaly-svc** - Real-time anomaly detection (reference models)
- **threat-forecastor** - ML-powered threat assessment (reference model)
- **trajectory-embedding** - Trajectory vectorization with caching
- **nlq-svc** - Natural language to SQL translation (Bulgarian + English)

### Observability
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards and visualization
- **Alert Rules** - Pre-configured for ML pipeline and Redis

## 📊 Project Status

| Aspect | Status |
|--------|--------|
| **Maturity** | Tech Preview / Alpha |
| **Scope** | Core 4D database, reference AI services, observability |
| **Not included** | Domain-specific modules (radar, ADS-B, vision GPU, NetGuardian) - see Full Edition |

## 🎯 Use Cases & Example Modules

Atlas4D Base ships with the core 4D engine and generic AI services. On top of this core, domain-specific modules can be added:

### Telecom & Networks
- GPON / fiber anomaly detection
- Capacity & congestion forecasting
- Network Guardian-style risk scoring for critical infrastructure

### Smart City & Mobility
- Traffic & fleet analytics via trajectories
- Movement anomalies (speed spikes, unusual routes)
- High-risk zones (stadiums, events, gatherings)

### Airspace & Airports
- Trajectory monitoring for aircraft and drones
- Conflict zones / separation violation detection
- Safety dashboards for control rooms

### Wildfires & Agriculture
- Fire risk mapping (wind, temperature, drought, historical fires)
- Crop yield forecasting on H3 grid
- Early warning for extreme weather events

### Defense & Security
- Multi-sensor drone detection (radar + vision + RF)
- Spatiotemporal analysis of suspicious objects and vehicles
- Pattern-of-life analysis on 4D trajectories

### Predictive Analytics
- Time-series forecasting
- Vector-based similarity: "find trajectories similar to this incident"

## 📚 Documentation

- [Quick Start Guide](docs/quickstart/QUICK_START.md)
- [Architecture Overview](docs/architecture/ARCHITECTURE.md)
- [Database Schema](docs/architecture/SCHEMA.md)
- [API Reference](docs/api/API_REFERENCE.md)
- [NLQ Usage Guide](docs/api/NLQ_USAGE.md)
- [STSQL Overview](docs/api/STSQL_OVERVIEW.md)

## 🔧 Configuration
```yaml
# .env.example
POSTGRES_HOST=postgres
POSTGRES_DB=atlas4d
POSTGRES_USER=atlas4d_app
POSTGRES_PASSWORD=your_secure_password

# Optional: Enable ML features
ENABLE_ANOMALY_DETECTION=true
ENABLE_THREAT_FORECAST=true
ENABLE_NLQ=true
```

## 🗺️ Roadmap

- [x] Core spatiotemporal database schema
- [x] H3 hexagonal indexing
- [x] Anomaly detection pipeline
- [x] Embedding cache with Redis
- [x] Natural language queries (Bulgarian + English)
- [x] E2E demo test suite
- [ ] Kubernetes Helm charts
- [ ] Multi-tenant support
- [ ] Real-time WebSocket feeds

## 🤝 Atlas4D Full Edition

This is **Atlas4D Base** - the open-source foundation and reference implementation.

**Atlas4D Full Edition** includes additional enterprise modules built on top of this base:

- **Radar & ADS-B fusion** for airspace monitoring
- **Drone & low-altitude threat detection**
- **Telco Network Guardian** (fiber/ISP network analytics)
- **GPU-accelerated vision** and video analytics
- **Advanced forecasting** (multi-source risk scoring, LSTM models)
- **SLA-grade support**, sizing and deployment guidance

[Contact us](mailto:cris@digicom.bg) for enterprise inquiries.

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## 🙏 Built On

Atlas4D stands on the shoulders of giants:
- [PostgreSQL](https://postgresql.org)
- [PostGIS](https://postgis.net)
- [TimescaleDB](https://timescale.com)
- [H3](https://h3geo.org)
- [pgvector](https://github.com/pgvector/pgvector)

---

**Our vision:** Atlas4D aims to become the "Linux of 4D spatiotemporal data platforms" - a stable, open foundation for location-aware, time-sensitive AI applications.

⭐ Star this repo if you find it useful!

### 💬 Ask Your Data in Natural Language

Atlas4D supports natural language queries in Bulgarian and English:

**Bulgarian:**
- "Какво е времето в Бургас?"
- "Покажи заплахи около София"
- "Покажи аномалии от последния час"

**English:**
- "Show threats near the airport"
- "What anomalies happened today?"

See [NLQ Usage Guide](docs/api/NLQ_USAGE.md) for full examples.

## 🔗 After the Stack is Up

| Service | URL |
|---------|-----|
| **Map UI** | http://localhost:8091 |
| **API** | http://localhost:8090/api/observations |
| **Health** | http://localhost:8090/health |
| **Stats** | http://localhost:8090/api/stats |
