# Atlas4D Python SDK

[![PyPI version](https://badge.fury.io/py/atlas4d.svg)](https://badge.fury.io/py/atlas4d)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Python client for [Atlas4D](https://atlas4d.tech) - Open 4D Spatiotemporal AI Platform.

## Installation
```bash
pip install atlas4d
```

## Quick Start
```python
from atlas4d import Client

# Connect to Atlas4D
client = Client(host="localhost", port=8090)

# Check health
print(client.health())

# Get statistics
print(client.stats())

# Query observations
observations = client.observations.list(
    lat=42.5,
    lon=27.46,
    radius_km=10,
    hours=24,
    limit=100
)

# Query anomalies
anomalies = client.anomalies.list(hours=24)
```

## Context Manager
```python
from atlas4d import Client

with Client() as client:
    print(client.stats())
# Session automatically closed
```

## Environment Variables

Configure connection via environment:
```bash
export ATLAS4D_HOST=192.168.1.100
export ATLAS4D_PORT=8090
```
```python
from atlas4d import Client

# Uses ATLAS4D_HOST and ATLAS4D_PORT from environment
client = Client()
```

## API Reference

### Client

| Method | Description |
|--------|-------------|
| `health()` | Check API health status |
| `stats()` | Get platform statistics |
| `close()` | Close the session |

### client.observations

| Method | Description |
|--------|-------------|
| `list(...)` | Query observations with filters |
| `geojson(...)` | Get observations as GeoJSON |

### client.anomalies

| Method | Description |
|--------|-------------|
| `list(...)` | Query anomalies with filters |

## Links

- **Homepage:** https://atlas4d.tech
- **GitHub:** https://github.com/crisbez/atlas4d-base
- **Documentation:** https://github.com/crisbez/atlas4d-base/tree/main/sdk/python
- **Issues:** https://github.com/crisbez/atlas4d-base/issues

## License

Apache 2.0 - see [LICENSE](https://github.com/crisbez/atlas4d-base/blob/main/LICENSE)
