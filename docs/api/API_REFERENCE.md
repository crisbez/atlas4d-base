# Atlas4D Base - API Reference

## Overview

Atlas4D exposes RESTful APIs for data ingestion, queries, and ML services.

**Base URL:** `http://localhost:8080/api`

---

## Authentication
```bash
# Get JWT token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

---

## Core Endpoints

### Health Check
```
GET /health
```
Returns service health status.

### Observations

#### Ingest Observation
```
POST /api/observations
Content-Type: application/json

{
  "lat": 42.5,
  "lon": 27.46,
  "t": "2025-12-01T10:00:00Z",
  "source_type": "sensor",
  "metadata": {}
}
```

#### Query Observations
```
GET /api/observations?lat=42.5&lon=27.46&radius_km=10&hours=24
```

---

## ML Services

### Threat Forecast
```
POST /api/forecast
Content-Type: application/json

{
  "lat": 42.5,
  "lon": 27.46
}
```

Response:
```json
{
  "threat_level": "low",
  "threat_score": 0.15,
  "h3_cell": "891e2a5..."
}
```

### Anomaly Detection
```
GET /api/anomalies/recent?limit=100
```

---

## NLQ (Natural Language Query)
```
POST /api/nlq/universal
Content-Type: application/json

{
  "query": "Show anomalies in Burgas",
  "language": "en"
}
```

---

## Rate Limits

- Default: 100 requests/minute per IP
- Authenticated: 1000 requests/minute

---

*Full API documentation available in Atlas4D Full Edition.*
