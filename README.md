# 🌐 Atlas4D Base

**Open 4D Spatiotemporal AI Platform built on PostgreSQL**

Atlas4D is a ready-to-run platform for real-time spatiotemporal intelligence, combining PostGIS, TimescaleDB, H3 hexagonal indexing, and pgvector for unified geospatial-temporal-vector analytics.

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
open http://localhost:8080/ui/
```

**Time to first map: ~5 minutes**

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

## 🎯 Use Cases

- **Telecom Network Monitoring** - Detect anomalies across network infrastructure
- **Smart City** - Real-time urban mobility and safety analytics
- **Fleet Management** - Trajectory analysis and threat zones
- **Critical Infrastructure** - Spatiotemporal threat assessment

## 📚 Documentation

- [Quick Start Guide](docs/quickstart/QUICK_START.md)
- [Architecture Overview](docs/architecture/ARCHITECTURE.md)
- [Database Schema](docs/architecture/SCHEMA.md)
- [API Reference](docs/api/API_REFERENCE.md)

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

**Atlas4D Full Edition** includes additional enterprise features:
- Advanced ML models (LSTM threat prediction, extended feature set)
- Network Guardian module
- Radar/ADS-B integration
- GPU-accelerated vision processing
- Production deployment support

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
