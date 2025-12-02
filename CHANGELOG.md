# Changelog

All notable changes to Atlas4D Base will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.3.0] - 2025-12-02

### Summary
First public release of Atlas4D Base - the open 4D spatiotemporal stack.

### Added
- **Core Stack**: PostgreSQL 16 with PostGIS, TimescaleDB, pgvector, H3
- **API Gateway**: FastAPI with asyncpg, health checks, CORS
- **Frontend**: Leaflet map with scenario toggle
- **Demo Scenarios**: Burgas mobility (500 obs) + Telecom network (78 obs)
- **Documentation**:
  - Quick Start guide
  - Developer Onboarding
  - Contributing guidelines
  - Core Specification (v0.3)
  - Module Model
  - Ecosystem Positioning
  - Blog draft: "Why Atlas4D"
  - Web Content Pack (ONE_PAGER, USE_CASES, SLIDES)

### Core Components
| Component | Version |
|-----------|---------|
| PostgreSQL | 16 |
| PostGIS | 3.4 |
| TimescaleDB | latest |
| pgvector | 0.5+ |
| Redis | 7 |

### API Endpoints
- `GET /health` - Service health
- `GET /api/stats` - Platform statistics
- `GET /api/observations` - Query observations
- `POST /api/observations` - Create observation
- `GET /api/anomalies` - Query anomalies
- `GET /api/geojson/observations` - Map-ready GeoJSON

### Known Limitations
- Single-node deployment only
- No authentication (add reverse proxy for production)
- NLQ service not included in Base (see full platform)

---

## [0.2.0] - 2025-11 (Internal)

- Initial docker-compose structure
- Basic schema design

## [0.1.0] - 2025-10 (Internal)

- Project inception
- Technology selection

---

[0.3.0]: https://github.com/crisbez/atlas4d-base/releases/tag/v0.3.0
