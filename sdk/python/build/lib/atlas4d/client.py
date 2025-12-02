"""
Atlas4D Python Client

Simple, synchronous client for Atlas4D Base API.
No magic, no async - just requests.
"""

import os
import requests
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin


class ObservationsAPI:
    """Observations endpoint wrapper"""
    
    def __init__(self, client: 'Client'):
        self._client = client
    
    def list(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius_km: float = 10,
        hours: int = 24,
        source_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        params = {"radius_km": radius_km, "hours": hours, "limit": limit}
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if source_type:
            params["source_type"] = source_type
        return self._client._get("/api/observations", params=params)
    
    def geojson(self, limit: int = 100) -> Dict[str, Any]:
        return self._client._get("/api/geojson/observations", params={"limit": limit})


class AnomaliesAPI:
    """Anomalies endpoint wrapper"""
    
    def __init__(self, client: 'Client'):
        self._client = client
    
    def list(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        return self._client._get("/api/anomalies", params={"hours": hours, "limit": limit})


class Client:
    """
    Atlas4D API Client
    
    Example:
        >>> from atlas4d import Client
        >>> with Client() as client:
        ...     print(client.stats())
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        timeout: int = 30
    ):
        self.host = host or os.getenv("ATLAS4D_HOST", "localhost")
        self.port = port or int(os.getenv("ATLAS4D_PORT", "8090"))
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = timeout
        self._session = requests.Session()
        self.observations = ObservationsAPI(self)
        self.anomalies = AnomaliesAPI(self)
    
    def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        url = urljoin(self.base_url, path)
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def health(self) -> Dict[str, Any]:
        return self._get("/health")
    
    def stats(self) -> Dict[str, Any]:
        return self._get("/api/stats")
    
    def close(self):
        self._session.close()
    
    def __enter__(self) -> 'Client':
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def __repr__(self) -> str:
        return f"Client(host='{self.host}', port={self.port})"
