# Atlas4D Python SDK
```python
from atlas4d import Client

with Client() as client:
    print(client.health())
    print(client.stats())
    
    obs = client.observations.list(limit=10)
    anomalies = client.anomalies.list(hours=24)
```

## Install
```bash
pip install ./sdk/python
```

## Environment Variables
```bash
export ATLAS4D_HOST=localhost
export ATLAS4D_PORT=8090
```
