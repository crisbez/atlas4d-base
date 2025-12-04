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
    async with AsyncClient(host="localhost", port=8090) as client:
        # Ask documentation questions
        answer = await client.ask("How do I deploy Atlas4D?")
        print(answer.text)
        
        # Get observations
        obs = await client.observations.list(limit=100)
        print(f"Found {len(obs)} observations")

asyncio.run(main())
```

## Endpoint Configuration

Atlas4D deployments typically expose different endpoints:

| Endpoint | Default Port | Features |
|----------|--------------|----------|
| **Core API** | 8090 | Health, stats, observations, anomalies |
| **Full Platform** | 8081* | All above + NLQ, RAG, advanced features |

*Full platform endpoints are accessed via API gateway proxy.

### Configuration Options
```python
# Option 1: Environment variables (recommended for production)
# export ATLAS4D_HOST=myserver.com
# export ATLAS4D_PORT=8090
client = Client()  # Uses env vars automatically

# Option 2: Explicit configuration
client = Client(host="myserver.com", port=8090, timeout=60)

# Option 3: For RAG/NLQ features on full platform
client = Client(host="myserver.com", port=8081)
```

### Which Port Should I Use?

- **8090** - For basic operations (health, observations, anomalies)
- **8081** - For RAG/NLQ features (if deployed with full platform)

When in doubt, check your deployment's documentation or try:
```python
client = Client(host="your-server", port=8090)
print(client.health())  # Should return {"status": "healthy", ...}
```

## RAG (Documentation Q&A)

Ask questions about Atlas4D documentation in natural language:
```python
# English
answer = client.ask("What is Atlas4D Core?")
print(answer.text)

# Bulgarian  
answer = client.ask("Какво е Atlas4D?", lang="bg")

# With more sources
answer = client.ask("How to deploy?", top_k=5)

# Access sources
for source in answer.sources:
    print(f"- {source['doc_id']}: {source['similarity']:.0%}")
```

### RAGAnswer Object
```python
answer = client.ask("What is Atlas4D?")

answer.text        # The answer text
answer.sources     # List of source documents
answer.chunks_used # Number of chunks used for context
```

## Error Handling
```python
from atlas4d import Client
import requests

client = Client(host="localhost", port=8090)

try:
    health = client.health()
except requests.exceptions.ConnectionError:
    print("Cannot connect to Atlas4D server")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
```

### Async Error Handling
```python
from atlas4d import AsyncClient
import httpx

async def safe_query():
    try:
        async with AsyncClient() as client:
            return await client.ask("What is Atlas4D?")
    except httpx.ConnectError:
        print("Cannot connect to Atlas4D server")
    except httpx.TimeoutException:
        print("Request timed out")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
```

## API Reference

### Client / AsyncClient

| Method | Description |
|--------|-------------|
| `health()` | Check API health |
| `stats()` | Get platform statistics |
| `ask(question, top_k=3, lang="en")` | Ask documentation questions (RAG) |

### Observations API

| Method | Description |
|--------|-------------|
| `list(lat, lon, radius_km, hours, limit)` | List observations |
| `geojson(limit)` | Get as GeoJSON |

### Anomalies API

| Method | Description |
|--------|-------------|
| `list(hours, limit)` | List anomalies |

### RAG API

| Method | Description |
|--------|-------------|
| `query(question, top_k, lang)` | Full RAG query (same as `ask()`) |

## Examples

### Fetch Recent Activity
```python
from atlas4d import Client

client = Client(host="localhost", port=8090)

# Get observations from last hour
recent = client.observations.list(hours=1, limit=50)
print(f"Last hour: {len(recent)} observations")

# Get as GeoJSON for mapping
geojson = client.observations.geojson(limit=100)
print(f"GeoJSON features: {len(geojson['features'])}")
```

### Interactive Documentation Search
```python
from atlas4d import Client

client = Client(host="localhost", port=8081)  # Full platform

questions = [
    "How do I install Atlas4D?",
    "What databases does Atlas4D use?",
    "How to create a custom module?",
]

for q in questions:
    answer = client.ask(q)
    print(f"Q: {q}")
    print(f"A: {answer.text[:200]}...")
    print()
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Links

- [Atlas4D Website](https://atlas4d.tech)
- [GitHub Repository](https://github.com/crisbez/atlas4d-base)
- [PyPI Package](https://pypi.org/project/atlas4d/)
- [Documentation](https://github.com/crisbez/atlas4d-base/tree/main/docs)

## License

Apache 2.0
