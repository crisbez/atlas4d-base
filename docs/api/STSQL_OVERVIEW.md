# STSQL - Spatiotemporal SQL

STSQL is Atlas4D's query language that extends SQL with spatiotemporal shortcuts.

## Overview

STSQL simplifies common spatiotemporal queries by providing intuitive syntax for time ranges, locations, and data types.

## Basic Syntax
```
FROM <source> [time_filter] [location_filter] [conditions] [LIMIT n]
```

## Data Sources

| Source | Description |
|--------|-------------|
| `OBSERVATIONS` | Raw sensor/entity observations |
| `ANOMALIES` | Detected anomalies |
| `THREATS` | Threat assessments |
| `TRAJECTORIES` | Movement paths |
| `FUSIONS` | Correlated anomalies |

## Time Filters
```sql
-- Relative time
LAST 1h          -- Last hour
LAST 24h         -- Last 24 hours
LAST 7d          -- Last 7 days

-- Absolute time
AFTER '2025-01-01'
BEFORE '2025-01-31'
BETWEEN '2025-01-01' AND '2025-01-31'
```

## Location Filters
```sql
-- Near a point (lat, lon)
NEAR 42.5,27.5              -- Default 10km radius
NEAR 42.5,27.5 RADIUS 5km   -- Custom radius

-- Named locations
NEAR BURGAS
NEAR SOFIA
NEAR 'Black Sea Port'

-- Bounding box
IN BBOX 42.0,27.0,43.0,28.0
```

## Conditions
```sql
WHERE severity > 3
WHERE source_type = 'vehicle'
WHERE speed_ms > 20
WHERE anomaly_type IN ('speed_spike', 'unusual_route')
```

## Examples

### Basic Queries
```sql
-- All observations from last hour
FROM OBSERVATIONS LAST 1h

-- Anomalies near Burgas
FROM ANOMALIES NEAR BURGAS LAST 24h

-- High-severity threats
FROM THREATS WHERE severity > 3 LAST 7d

-- Vehicle observations
FROM OBSERVATIONS WHERE source_type = 'vehicle' LAST 1h
```

### Complex Queries
```sql
-- Speed anomalies near airport in last 6 hours
FROM ANOMALIES 
WHERE anomaly_type = 'speed_spike'
NEAR 42.57,27.52 RADIUS 5km
LAST 6h
LIMIT 50

-- Trajectory analysis for specific track
FROM TRAJECTORIES 
WHERE track_id = 'abc-123'
LAST 24h

-- Fused anomalies with high correlation
FROM FUSIONS
WHERE correlation_score > 0.8
LAST 12h
```

### Aggregations
```sql
-- Count anomalies by type
FROM ANOMALIES LAST 24h
GROUP BY anomaly_type

-- Average speed by source
FROM OBSERVATIONS LAST 1h
GROUP BY source_type
AGG avg(speed_ms)
```

## Response Format
```json
{
  "query": "FROM OBSERVATIONS LAST 1h NEAR BURGAS",
  "translated_sql": "SELECT * FROM atlas4d.observations_core WHERE...",
  "results": [...],
  "count": 142,
  "execution_time_ms": 45
}
```

## Integration with NLQ

Natural language queries are translated to STSQL internally:

| NLQ | STSQL |
|-----|-------|
| "Покажи аномалии в Бургас" | `FROM ANOMALIES NEAR BURGAS LAST 24h` |
| "Show threats from last hour" | `FROM THREATS LAST 1h` |
| "Vehicle observations near port" | `FROM OBSERVATIONS WHERE source_type='vehicle' NEAR 42.5,27.5` |

## Performance Tips

1. **Always use LIMIT** for large datasets
2. **Add time filters** to reduce scan range
3. **Use location filters** when possible
4. **Prefer specific source types** over scanning all

## API Endpoint
```
POST /api/stsql/execute
Content-Type: application/json

{
  "query": "FROM OBSERVATIONS LAST 1h NEAR BURGAS LIMIT 100"
}
```

## Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown source` | Invalid FROM target | Use: OBSERVATIONS, ANOMALIES, etc. |
| `Invalid time format` | Bad time filter | Use: LAST 1h, LAST 24h, etc. |
| `Location not found` | Unknown place name | Use coordinates or known cities |
