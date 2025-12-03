"""
Atlas4D Python Client
Simple, synchronous client for Atlas4D Base API.
No magic, no async - just requests.
"""
import os
import requests
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin
from dataclasses import dataclass


@dataclass
class RAGAnswer:
    """Response from RAG query."""
    text: str
    sources: List[Dict[str, Any]]
    chunks_used: int
    
    def __repr__(self) -> str:
        return f"RAGAnswer(text='{self.text[:50]}...', sources={len(self.sources)})"


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


class RAGAPI:
    """RAG (Retrieval-Augmented Generation) endpoint wrapper for documentation Q&A."""
    def __init__(self, client: 'Client'):
        self._client = client

    def query(
        self,
        question: str,
        top_k: int = 3,
        lang: str = "en"
    ) -> RAGAnswer:
        """
        Ask a question about Atlas4D documentation.
        
        Args:
            question: Your question in natural language
            top_k: Number of source documents to retrieve (default: 3)
            lang: Language for response - "en" or "bg" (default: "en")
        
        Returns:
            RAGAnswer with text, sources, and chunks_used
        
        Example:
            >>> answer = client.rag.query("How do I create a module?")
            >>> print(answer.text)
            >>> for source in answer.sources:
            ...     print(f"  - {source['doc_id']}: {source['similarity']:.0%}")
        """
        data = self._client._post("/api/nlq/rag", json={
            "q": question,
            "top_k": top_k,
            "lang": lang
        })
        return RAGAnswer(
            text=data.get("answer", ""),
            sources=data.get("sources", []),
            chunks_used=data.get("chunks_used", 0)
        )


class Client:
    """
    Atlas4D API Client
    
    Example:
        >>> from atlas4d import Client
        >>> client = Client()
        >>> 
        >>> # Health check
        >>> print(client.health())
        >>> 
        >>> # Ask documentation questions
        >>> answer = client.ask("How do I deploy Atlas4D?")
        >>> print(answer.text)
        >>> 
        >>> # Get observations
        >>> obs = client.observations.list(lat=42.5, lon=27.5, radius_km=10)
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
        
        # API endpoints
        self.observations = ObservationsAPI(self)
        self.anomalies = AnomaliesAPI(self)
        self.rag = RAGAPI(self)

    def _get(self, path: str, params: Optional[Dict] = None) -> Any:
        url = urljoin(self.base_url, path)
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, json: Optional[Dict] = None) -> Any:
        url = urljoin(self.base_url, path)
        response = self._session.post(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def health(self) -> Dict[str, Any]:
        """Check API health status."""
        return self._get("/health")

    def stats(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return self._get("/api/stats")

    def ask(
        self,
        question: str,
        top_k: int = 3,
        lang: str = "en"
    ) -> RAGAnswer:
        """
        Ask a question about Atlas4D documentation.
        
        Shortcut for client.rag.query()
        
        Args:
            question: Your question in natural language
            top_k: Number of source documents to retrieve (default: 3)
            lang: Language for response - "en" or "bg" (default: "en")
        
        Returns:
            RAGAnswer with text, sources, and chunks_used
        
        Example:
            >>> answer = client.ask("What is Atlas4D Core?")
            >>> print(answer.text)
            To deploy Atlas4D using Docker, follow these steps...
            
            >>> print(answer.sources)
            [{'doc_id': 'QUICK_START', 'section': '...', 'similarity': 0.85}]
        """
        return self.rag.query(question, top_k=top_k, lang=lang)

    def close(self):
        """Close the HTTP session."""
        self._session.close()

    def __enter__(self) -> 'Client':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self) -> str:
        return f"Client(host='{self.host}', port={self.port})"
