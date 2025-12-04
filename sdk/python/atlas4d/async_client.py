"""
Atlas4D Async Python Client
Async client using httpx for Atlas4D Base API.
"""
import os
from typing import Optional, List, Dict, Any
import httpx
from dataclasses import dataclass


@dataclass
class RAGAnswer:
    """Response from RAG query."""
    text: str
    sources: List[Dict[str, Any]]
    chunks_used: int
    
    def __repr__(self) -> str:
        return f"RAGAnswer(text='{self.text[:50]}...', sources={len(self.sources)})"


class AsyncObservationsAPI:
    """Async Observations endpoint wrapper"""
    def __init__(self, client: 'AsyncClient'):
        self._client = client

    async def list(
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
        return await self._client._get("/api/observations", params=params)

    async def geojson(self, limit: int = 100) -> Dict[str, Any]:
        return await self._client._get("/api/geojson/observations", params={"limit": limit})


class AsyncAnomaliesAPI:
    """Async Anomalies endpoint wrapper"""
    def __init__(self, client: 'AsyncClient'):
        self._client = client

    async def list(self, hours: int = 24, limit: int = 100) -> List[Dict[str, Any]]:
        return await self._client._get("/api/anomalies", params={"hours": hours, "limit": limit})


class AsyncRAGAPI:
    """Async RAG endpoint wrapper"""
    def __init__(self, client: 'AsyncClient'):
        self._client = client

    async def query(
        self,
        question: str,
        top_k: int = 3,
        lang: str = "en"
    ) -> RAGAnswer:
        """Ask a question about Atlas4D documentation."""
        data = await self._client._post("/api/nlq/rag", json={
            "q": question,
            "top_k": top_k,
            "lang": lang
        })
        return RAGAnswer(
            text=data.get("answer", ""),
            sources=data.get("sources", []),
            chunks_used=data.get("chunks_used", 0)
        )


class AsyncClient:
    """
    Atlas4D Async API Client
    
    Example:
        >>> from atlas4d import AsyncClient
        >>> async with AsyncClient() as client:
        ...     answer = await client.ask("How do I deploy?")
        ...     print(answer.text)
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        timeout: float = 30.0
    ):
        self.host = host or os.getenv("ATLAS4D_HOST", "localhost")
        self.port = port or int(os.getenv("ATLAS4D_PORT", "8090"))
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        
        self.observations = AsyncObservationsAPI(self)
        self.anomalies = AsyncAnomaliesAPI(self)
        self.rag = AsyncRAGAPI(self)

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        return self._client

    async def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        client = await self._ensure_client()
        response = await client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    async def _post(self, path: str, json: Optional[Dict] = None) -> Any:
        client = await self._ensure_client()
        response = await client.post(path, json=json)
        response.raise_for_status()
        return response.json()

    async def health(self) -> Dict[str, Any]:
        return await self._get("/health")

    async def stats(self) -> Dict[str, Any]:
        return await self._get("/api/stats")

    async def ask(self, question: str, top_k: int = 3, lang: str = "en") -> RAGAnswer:
        return await self.rag.query(question, top_k=top_k, lang=lang)

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> 'AsyncClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncClient(host='{self.host}', port={self.port})"
