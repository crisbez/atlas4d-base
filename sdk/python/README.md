# Atlas4D Python SDK

Simple Python client for [Atlas4D](https://atlas4d.tech) spatiotemporal platform.

## Installation
```bash
pip install atlas4d
```

**Requires Python 3.9+**

## Quick Start

### Sync Client
```python
from atlas4d import Client

# Connect to Atlas4D
client = Client(host="localhost", port=8090)

# Check health
print(client.health())

# Ask documentation questions (RAG)
answer = client.ask("How do I create a module?")
print(answer.text)
print(f"Sources: {len(answer.sources)}")

# Get observations
obs = client.observations.list(
    lat=42.5, 
    lon=27.5, 
    radius_km=10,
    hours=24
)
print(f"Found {len(obs)} observations")

# Get anomalies
anomalies = client.anomalies.list(hours=24)
```

### Async Client
```python
import asyncio
from atlas4d import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Ask documentation questions
        answer = await client.ask("How do I deploy Atlas4D?")
        print(answer.text)
        
        # Get observations
        obs = await client.observations.list(limit=100)
        print(f"Found {len(obs)} observations")

asyncio.run(main())
```

## Configuration
```python
# Using environment variables
# ATLAS4D_HOST=myserver.com
# ATLAS4D_PORT=8090

client = Client()  # Uses env vars

# Or explicit configuration
client = Client(host="myserver.com", port=8090, timeout=60)
```

## RAG (Documentation Q&A)

Ask questions about Atlas4D documentation in natural language:
```python
# English
answer = client.ask("What is Atlas4D Core?")

# Bulgarian
answer = client.ask("Какво е Atlas4D?", lang="bg")

# With more sources
answer = client.ask("How to deploy?", top_k=5)

# Access sources
for source in answer.sources:
    print(f"- {source['doc_id']}: {source['similarity']:.0%}")
```

## API Reference

### Client / AsyncClient

| Method | Description |
|--------|-------------|
| `health()` | Check API health |
| `stats()` | Get platform statistics |
| `ask(question, top_k=3, lang="en")` | Ask documentation questions |

### Observations API

| Method | Description |
|--------|-------------|
| `list(lat, lon, radius_km, hours, limit)` | List observations |
| `geojson(limit)` | Get as GeoJSON |

### Anomalies API

| Method | Description |
|--------|-------------|
| `list(hours, limit)` | List anomalies |

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Links

- [Atlas4D Website](https://atlas4d.tech)
- [GitHub Repository](https://github.com/crisbez/atlas4d-base)
- [Documentation](https://github.com/crisbez/atlas4d-base/tree/main/docs)

## License

Apache 2.0
