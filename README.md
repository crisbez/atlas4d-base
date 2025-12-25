# 🌐 Atlas4D Base

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) [![Version](https://img.shields.io/badge/Version-0.3.0-brightgreen)](CHANGELOG.md) [![PyPI](https://img.shields.io/pypi/v/atlas4d)](https://pypi.org/project/atlas4d/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://postgresql.org) [![PostGIS](https://img.shields.io/badge/PostGIS-3.4-green)](https://postgis.net) [![TimescaleDB](https://img.shields.io/badge/TimescaleDB-latest-orange)](https://timescale.com) [![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](docker-compose.yml)

**Open 4D Spatiotemporal AI Platform built on PostgreSQL**

> 📰 **Featured:** [Why We Built Atlas4D](https://dev.to/crisbez/why-we-built-atlas4d-the-missing-4d-data-platform-5787) — The problem with fragmented spatiotemporal data and how we solved it.

## 🏆 Recognition

[![Awesome](https://awesome.re/badge.svg)](https://github.com/sacridini/Awesome-Geospatial) [![Awesome PostgreSQL](https://img.shields.io/badge/Awesome-PostgreSQL-336791?logo=postgresql)](https://github.com/dhamaniasad/awesome-postgres)

**As seen in:**
- [Awesome-PostgreSQL](https://github.com/dhamaniasad/awesome-postgres) - The definitive PostgreSQL resource list (Platforms category) 🆕
- [Awesome-Geospatial](https://github.com/sacridini/Awesome-Geospatial) - Curated list of geospatial resources

Atlas4D Base is the **open-core** of the larger Atlas4D platform. This repo contains a minimal but fully working 4D stack - database, core services, and observability. The full Atlas4D platform adds extra domain modules (radar, drones, telco network analytics, etc.).

## 👥 Who Is This For?

- **Data Engineers** building real-time spatiotemporal pipelines
- **GIS/Geo Developers** needing time-series + vector search in one DB
- **Telecom Teams** monitoring network infrastructure
- **Smart City Projects** analyzing mobility and urban data
- **Research Labs** working with 4D trajectory data


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
# Clone and start
git clone https://github.com/crisbez/atlas4d-base.git
cd atlas4d-base
make demo
```

Or manually:
```bash
cp .env.example .env
docker compose up -d --build
```

**⏱️ Time to first map: ~3 minutes**

| Service | URL |
|---------|-----|
| Map UI | http://localhost:8091 |
| API Health | http://localhost:8090/health |
| API Stats | http://localhost:8090/api/stats |

![Demo Map](docs/quickstart/img/demo_burgas_map.png)


## 🌐 Live Demo

Try Atlas4D without installing:

| Service | URL |
|---------|-----|
| **Map UI** | [atlas4d-demo.digicom.bg:8091](http://185.18.56.13:8091) |
| **API Health** | [/health](http://185.18.56.13:8090/health) |
| **API Stats** | [/api/stats](http://185.18.56.13:8090/api/stats) |
| **Observations** | [/api/observations](http://185.18.56.13:8090/api/observations?limit=10) |

> 💡 Demo resets daily with fresh Burgas mobility data.

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

## 🔒 Security & Hardening

Atlas4D Base ships with a **developer-friendly demo configuration**.  
It is not production-ready out of the box.

Before exposing a deployment to the internet you should:

- change all default passwords and secrets,
- restrict exposed ports and put Atlas4D behind a reverse proxy (HTTPS),
- use a dedicated DB user with least privilege,
- protect observability (Grafana/Prometheus) and internal APIs.

See [`docs/SECURITY.md`](docs/SECURITY.md) for a detailed hardening guide.

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

[Contact us](mailto:office@atlas4d.tech) for enterprise inquiries.




## 📊 Case Studies

Atlas4D is designed for multiple industries. Explore our use case outlines:

| Industry | Use Case | Key Features |
|----------|----------|--------------|
| 📡 **Telecom** | [Network Monitoring](docs/case-studies/TELECOM_BURGAS_OUTLINE.md) | SNMP, GPON, real-time alerts |
| 🏙️ **Smart City** | [Municipal IoT Platform](docs/case-studies/SMART_CITY_OUTLINE.md) | Traffic, parking, air quality |
| 🛡️ **Defense** | [Counter-Drone System](docs/case-studies/DRONE_DEFENSE_OUTLINE.md) | Radar fusion, swarm detection |
| 🔥 **Emergency** | [Wildfire Monitoring](docs/case-studies/WILDFIRE_MONITORING_OUTLINE.md) | Risk prediction, satellite hotspots |
| 🌾 **Agriculture** | [Harvest Forecasting](docs/case-studies/AGRICULTURE_WHEAT_OUTLINE.md) | NDVI tracking, yield prediction |

Each case study includes architecture diagrams, NLQ examples (Bulgarian + English), and expected results.

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](docs/community/CONTRIBUTOR_PATHS.md).

**Ways to contribute:**
- 🐛 Report bugs
- 📝 Improve documentation
- 💻 Submit code
- 💡 Propose new modules

Check out our [Good First Issues](docs/community/GOOD_FIRST_ISSUES.md) for beginner-friendly tasks.

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
| **Map UI** | http://185.18.56.13:8091 |
| **API** | http://185.18.56.13:8090/api/observations |
| **Health** | http://185.18.56.13:8090/health |
| **Stats** | http://185.18.56.13:8090/api/stats |

---

## 👩‍💻 For Developers

New to Atlas4D Base? Start here:

- **[Developer Onboarding](docs/DEVELOPER_ONBOARDING.md)** - Architecture, first 10 minutes, common tasks
- **[Contributing Guide](CONTRIBUTING.md)** - How to submit PRs, code style, testing

### Quick Dev Commands
```bash
# Start stack
docker compose up -d

# View logs
docker compose logs -f api-gateway

# Connect to database
docker compose exec postgres psql -U atlas4d_app -d atlas4d

# Rebuild after changes
docker compose build api-gateway && docker compose up -d api-gateway
```

---

## 🗺️ Roadmap

See [ROADMAP.md](docs/ROADMAP.md) for upcoming features and releases.

**Current:** v0.3.0 | **Next:** v0.4.0 (Q1 2026) — Module Ecosystem
