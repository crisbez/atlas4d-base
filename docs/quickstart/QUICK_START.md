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

# Edit if needed (defaults work for local dev)
# nano .env
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
{"status": "healthy", "services": {...}}
```

## Step 4: Open the UI

Open your browser to: **http://localhost:8080/ui/**

You should see:
- Interactive map centered on Bulgaria
- Sample trajectory data
- Anomaly markers (if demo data loaded)

## Step 5: Load Demo Data (Optional)
```bash
# Load sample observations and trajectories
docker compose exec postgres psql -U atlas4d_app -d atlas4d -f /docker-entrypoint-initdb.d/demo_data.sql
```

## Step 6: Try NLQ (Natural Language Query)

Navigate to **http://localhost:8080/ui/nlq.html**

Try queries like:
- "Покажи аномалии в Бургас" (Show anomalies in Burgas)
- "What is the weather in Sofia?"
- "Show threats from last hour"

## Stopping Atlas4D
```bash
docker compose down

# To also remove data volumes:
docker compose down -v
```

## Next Steps

- [Architecture Overview](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Database Schema](SCHEMA.md)

## Troubleshooting

### Services won't start
```bash
# Check logs
docker compose logs -f

# Ensure ports 8080, 5432, 6379 are free
```

### Database connection errors
```bash
# Wait for postgres to be ready
docker compose logs postgres | tail -20
```

### Need help?
Open an issue on GitHub or email cris@digicom.bg
