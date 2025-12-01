#!/bin/bash
# Atlas4D Base - API Examples

BASE_URL="http://localhost:8080"

echo "=== Health Check ==="
curl -s $BASE_URL/health | jq

echo -e "\n=== Ingest Observation ==="
curl -s -X POST $BASE_URL/api/observations \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 42.5,
    "lon": 27.46,
    "t": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "source_type": "demo",
    "metadata": {"demo": true}
  }' | jq

echo -e "\n=== Query Observations ==="
curl -s "$BASE_URL/api/observations?lat=42.5&lon=27.46&radius_km=10" | jq

echo -e "\n=== Threat Forecast ==="
curl -s -X POST $BASE_URL/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"lat": 42.5, "lon": 27.46}' | jq

echo -e "\n=== NLQ Query ==="
curl -s -X POST $BASE_URL/api/nlq/universal \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in Burgas?"}' | jq
