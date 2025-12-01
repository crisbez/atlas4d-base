# Atlas4D Quick Start Guide

Get Atlas4D running in 5 minutes.

## Prerequisites

- Docker & Docker Compose
- 4GB RAM minimum
- 10GB disk space

## Step 1: Clone & Configure
```bash
git clone https://github.com/crisbez/atlas4d-base.git
cd atlas4d-base

# Copy example environment
cp .env.example .env
```

## Step 2: Start Services
```bash
docker compose up -d
```

Wait ~60 seconds for all services to initialize.

## Step 3: Verify Health
```bash
# Check all services are running
docker compose ps

# Test API health
curl http://localhost:8080/health
```

Expected response:
```json
{"status": "healthy"}
```

## Step 4: Load Demo Data (Optional)
```bash
# Load Burgas city demo scenario (500 observations, 30 anomalies)
docker compose exec postgres psql -U atlas4d_app -d atlas4d -f /docker-entrypoint-initdb.d/seed/demo_burgas.sql
```

## Step 5: Open the UI

Open your browser:

| Service | URL |
|---------|-----|
| Map UI | http://localhost:8080/ui/ |
| API Health | http://localhost:8080/health |
| API Docs | http://localhost:8080/docs |

## Step 6: Try NLQ (Natural Language Query)

Navigate to the NLQ interface and try:

**Bulgarian:**
- "Какво е времето в Бургас?"
- "Покажи аномалии от последния час"
- "Покажи заплахи близо до София"

**English:**
- "Show threats near Burgas"
- "What anomalies happened today?"
- "Show observations from last 24 hours"

## Demo Scenario: What You'll See

After loading the demo data, you'll have:

| Data Type | Count | Description |
|-----------|-------|-------------|
| Observations | ~500 | Vehicle, sensor, camera readings |
| Anomalies | ~30 | Speed spikes, unusual routes |
| Coverage | Burgas area | 42.5°N, 27.5°E ± 10km |

The map will show:
- 📍 Observation points colored by source type
- ⚠️ Anomaly markers with severity levels
- 🗺️ Burgas city area coverage

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
# Ensure ports 8080, 5432, 6379 are free
```

### Database connection errors
```bash
docker compose logs postgres | tail -20
```

### Need help?
- Open an issue on [GitHub](https://github.com/crisbez/atlas4d-base/issues)
- Email: cris@digicom.bg

## Next Steps

- [Architecture Overview](../architecture/ARCHITECTURE.md)
- [API Reference](../api/API_REFERENCE.md)
- [Database Schema](../architecture/SCHEMA.md)
- [NLQ Usage Guide](../api/NLQ_USAGE.md)
