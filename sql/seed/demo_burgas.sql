-- Atlas4D Base Demo Data: Burgas City Scenario
-- This script creates sample data for demonstration purposes

-- Ensure schema exists
CREATE SCHEMA IF NOT EXISTS atlas4d;

-- Sample entities (vehicles, sensors)
INSERT INTO atlas4d.observations_core (t, lat, lon, source_type, track_id, speed_ms, heading_deg, metadata)
SELECT 
    NOW() - (random() * INTERVAL '24 hours'),
    42.5 + (random() - 0.5) * 0.1,  -- Burgas area lat
    27.46 + (random() - 0.5) * 0.15, -- Burgas area lon
    CASE (random() * 3)::int 
        WHEN 0 THEN 'vehicle'
        WHEN 1 THEN 'sensor'
        ELSE 'camera'
    END,
    gen_random_uuid(),
    random() * 30,  -- 0-30 m/s speed
    random() * 360, -- heading
    jsonb_build_object('demo', true, 'source', 'seed_script')
FROM generate_series(1, 500);

-- Sample anomalies
INSERT INTO atlas4d.anomalies (observation_id, anomaly_type, severity, score, detected_at, metadata)
SELECT 
    id,
    CASE (random() * 4)::int
        WHEN 0 THEN 'speed_spike'
        WHEN 1 THEN 'unusual_route'
        WHEN 2 THEN 'stationary_alert'
        ELSE 'pattern_deviation'
    END,
    (random() * 4 + 1)::int,  -- severity 1-5
    random(),  -- score 0-1
    NOW() - (random() * INTERVAL '12 hours'),
    jsonb_build_object('demo', true)
FROM atlas4d.observations_core 
WHERE random() < 0.1  -- ~10% of observations become anomalies
LIMIT 30;

-- Verify
DO $$
DECLARE
    obs_count INT;
    anom_count INT;
BEGIN
    SELECT COUNT(*) INTO obs_count FROM atlas4d.observations_core WHERE metadata->>'demo' = 'true';
    SELECT COUNT(*) INTO anom_count FROM atlas4d.anomalies WHERE metadata->>'demo' = 'true';
    RAISE NOTICE 'Demo data loaded: % observations, % anomalies', obs_count, anom_count;
END $$;
