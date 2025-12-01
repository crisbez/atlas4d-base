# Atlas4D Database Schema

## Overview

Atlas4D uses PostgreSQL with several extensions:
- **PostGIS** - Spatial data types and functions
- **TimescaleDB** - Time-series optimization
- **H3** - Hexagonal hierarchical indexing
- **pgvector** - Vector similarity search

## Core Tables

### observations_core

The main table for all spatiotemporal observations.
```sql
CREATE TABLE atlas4d.observations_core (
    id              BIGSERIAL PRIMARY KEY,
    t               TIMESTAMPTZ NOT NULL,
    geom            GEOMETRY(Point, 4326),
    h3_index        H3INDEX,
    source_type     VARCHAR(50),
    track_id        UUID,
    entity_id       UUID,
    lat             DOUBLE PRECISION,
    lon             DOUBLE PRECISION,
    altitude_m      DOUBLE PRECISION,
    speed_ms        DOUBLE PRECISION,
    heading_deg     DOUBLE PRECISION,
    metadata        JSONB DEFAULT '{}'
);

-- TimescaleDB hypertable
SELECT create_hypertable('atlas4d.observations_core', 't', 
    chunk_time_interval => INTERVAL '1 day');

-- Indexes
CREATE INDEX idx_obs_h3 ON atlas4d.observations_core (h3_index);
CREATE INDEX idx_obs_track ON atlas4d.observations_core (track_id);
CREATE INDEX idx_obs_geom ON atlas4d.observations_core USING GIST (geom);
```

### trajectory_embeddings

Vector embeddings for trajectory similarity search.
```sql
CREATE TABLE atlas4d.trajectory_embeddings (
    id              SERIAL PRIMARY KEY,
    track_id        UUID NOT NULL,
    source_type     VARCHAR(50),
    start_time      TIMESTAMPTZ,
    end_time        TIMESTAMPTZ,
    point_count     INTEGER,
    embedding       VECTOR(768),
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- pgvector index for similarity search
CREATE INDEX idx_traj_emb_vector 
    ON atlas4d.trajectory_embeddings 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### anomalies

Detected anomalies from observations.
```sql
CREATE TABLE atlas4d.anomalies (
    id              SERIAL PRIMARY KEY,
    observation_id  BIGINT REFERENCES atlas4d.observations_core(id),
    anomaly_type    VARCHAR(50),
    severity        INTEGER CHECK (severity BETWEEN 1 AND 5),
    score           DOUBLE PRECISION,
    h3_index        H3INDEX,
    detected_at     TIMESTAMPTZ DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'
);
```

### fused_anomalies

Correlated anomalies from multiple sources.
```sql
CREATE TABLE atlas4d.fused_anomalies (
    fusion_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fusion_type     VARCHAR(50),
    anomaly_ids     BIGINT[],
    correlation_score DOUBLE PRECISION,
    threat_level    VARCHAR(20),
    h3_cell         H3INDEX,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

## H3 Functions
```sql
-- Get H3 index for a point
SELECT h3_lat_lng_to_cell(lat, lon, 9) AS h3_index;

-- Get neighbors
SELECT h3_grid_ring(h3_index, 1) AS neighbors;

-- Convert H3 to polygon for visualization
SELECT h3_cell_to_boundary_geometry(h3_index) AS boundary;
```

## Useful Queries

### Find observations in area
```sql
SELECT * FROM atlas4d.observations_core
WHERE ST_DWithin(
    geom::geography,
    ST_SetSRID(ST_MakePoint(27.46, 42.50), 4326)::geography,
    5000  -- meters
)
AND t > NOW() - INTERVAL '1 hour';
```

### Find similar trajectories
```sql
SELECT track_id, 
       1 - (embedding <=> query_embedding) AS similarity
FROM atlas4d.trajectory_embeddings
ORDER BY embedding <=> query_embedding
LIMIT 10;
```

### Aggregate by H3 cell
```sql
SELECT h3_index, 
       COUNT(*) as obs_count,
       AVG(speed_ms) as avg_speed
FROM atlas4d.observations_core
WHERE t > NOW() - INTERVAL '1 day'
GROUP BY h3_index
ORDER BY obs_count DESC;
```

## Extensions Setup
```sql
-- Required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS h3;
CREATE EXTENSION IF NOT EXISTS vector;

-- Schema
CREATE SCHEMA IF NOT EXISTS atlas4d;
```
