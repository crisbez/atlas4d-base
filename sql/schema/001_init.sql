-- Atlas4D Base Schema Initialization
-- Version: 1.0.0

-- Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS vector;

-- Note: H3 extension requires separate installation
-- CREATE EXTENSION IF NOT EXISTS h3;

-- Schema
CREATE SCHEMA IF NOT EXISTS atlas4d;

-- Core observations table
CREATE TABLE IF NOT EXISTS atlas4d.observations_core (
    id              BIGSERIAL PRIMARY KEY,
    t               TIMESTAMPTZ NOT NULL,
    geom            GEOMETRY(Point, 4326),
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

-- Convert to hypertable
SELECT create_hypertable('atlas4d.observations_core', 't', 
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_obs_track 
    ON atlas4d.observations_core (track_id);
CREATE INDEX IF NOT EXISTS idx_obs_source 
    ON atlas4d.observations_core (source_type);
CREATE INDEX IF NOT EXISTS idx_obs_geom 
    ON atlas4d.observations_core USING GIST (geom);

-- Trajectory embeddings
CREATE TABLE IF NOT EXISTS atlas4d.trajectory_embeddings (
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

-- Anomalies
CREATE TABLE IF NOT EXISTS atlas4d.anomalies (
    id              SERIAL PRIMARY KEY,
    observation_id  BIGINT,
    anomaly_type    VARCHAR(50),
    severity        INTEGER CHECK (severity BETWEEN 1 AND 5),
    score           DOUBLE PRECISION,
    detected_at     TIMESTAMPTZ DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'
);

-- Grant permissions
GRANT ALL ON SCHEMA atlas4d TO atlas4d_app;
GRANT ALL ON ALL TABLES IN SCHEMA atlas4d TO atlas4d_app;
GRANT ALL ON ALL SEQUENCES IN SCHEMA atlas4d TO atlas4d_app;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Atlas4D Base schema initialized successfully';
END $$;
