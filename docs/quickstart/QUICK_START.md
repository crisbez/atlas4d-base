# Atlas4D Quick Start Guide

Get Atlas4D Base running in 5 minutes.

## Prerequisites

- Docker & Docker Compose
- 4GB RAM minimum
- 10GB disk space

## Step 1: Clone & Start
```bash
git clone https://github.com/crisbez/atlas4d-base.git
cd atlas4d-base
docker compose up -d
```

Wait ~30 seconds for all services to initialize.

## Step 2: Verify Health
```bash
# Check all services are running
docker compose ps

# Test API health
curl http://localhost:8090/health
```

Expected response:
```json
{"status":"healthy","postgres":"healthy","redis":"healthy","version":"1.0.0"}
```

## Step 3: Load Demo Data
```bash
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f /docker-entrypoint-initdb.d/seed/demo_burgas.sql
```

Expected output:
```
NOTICE:  Demo data loaded: 500 observations, 30 anomalies
```

## Step 4: Open the Map

Open your browser: **http://localhost:8091**

You should see something like this:

![Atlas4D Base Demo Map](img/demo_burgas_map.png)

## Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Map UI** | http://localhost:8091 | Interactive map with observations |
| **API Health** | http://localhost:8090/health | Service health check |
| **API Stats** | http://localhost:8090/api/stats | Platform statistics |
| **API Observations** | http://localhost:8090/api/observations | Query observations |
| **API Anomalies** | http://localhost:8090/api/anomalies | Query anomalies |
| **API GeoJSON** | http://localhost:8090/api/geojson/observations | Map-ready data |

## Example API Calls

### Get Platform Stats
```bash
curl -s http://localhost:8090/api/stats | jq
```
```json
{
  "total_observations": 500,
  "total_anomalies": 30,
  "sources": {"sensor": 165, "camera": 251, "vehicle": 84},
  "last_observation": "2025-12-01T13:17:29Z"
}
```

### Query Observations
```bash
curl -s "http://localhost:8090/api/observations?limit=5" | jq
```

### Query Observations Near a Point
```bash
curl -s "http://localhost:8090/api/observations?lat=42.5&lon=27.46&radius_km=5&limit=50" | jq
```

### Get Anomalies
```bash
curl -s "http://localhost:8090/api/anomalies?hours=24&severity_min=3" | jq
```

### Get GeoJSON for Map
```bash
curl -s "http://localhost:8090/api/geojson/observations?hours=24&limit=500" | jq
```

### Create New Observation
```bash
curl -X POST http://localhost:8090/api/observations \
  -H "Content-Type: application/json" \
  -d '{"lat": 42.5, "lon": 27.46, "source_type": "manual"}'
```

## Demo Data Details

The Burgas demo scenario includes:

| Data Type | Count | Description |
|-----------|-------|-------------|
| Observations | 500 | Vehicle, sensor, camera readings |
| Anomalies | 30 | Speed spikes, unusual routes, pattern deviations |
| Coverage | Burgas area | 42.5°N, 27.46°E ± ~10km |
| Time Range | Last 24 hours | Randomly distributed |

### Source Types
- 🔵 **Vehicle** - Moving vehicles with speed/heading
- 🟢 **Sensor** - Fixed IoT sensors
- 🔴 **Camera** - Vision system detections
- 🟠 **Anomaly** - Detected anomalies (larger markers)

## Stopping Atlas4D
```bash
docker compose down

# To also remove data volumes:
docker compose down -v
```

## Troubleshooting

### Services won't start
```bash
docker compose logs -f
# Ensure ports 8090, 8091, 5433, 6380 are free
```

### Database connection errors
```bash
docker compose logs postgres | tail -20
```

### No data on map
```bash
# Verify demo data is loaded
curl -s http://localhost:8090/api/stats | jq
# If total_observations is 0, run the seed command again
```

### Port conflicts
If you have another service on these ports, edit `docker-compose.yml`:
- `8090` → API Gateway
- `8091` → Frontend
- `5433` → PostgreSQL
- `6380` → Redis

## Next Steps

- [Architecture Overview](../architecture/ARCHITECTURE.md)
- [API Reference](../api/API_REFERENCE.md)
- [Database Schema](../architecture/SCHEMA.md)
- [NLQ Usage Guide](../api/NLQ_USAGE.md)
- [STSQL Overview](../api/STSQL_OVERVIEW.md)

---

**Setup time: < 5 minutes** | **Questions?** Open an issue on [GitHub](https://github.com/crisbez/atlas4d-base/issues)
