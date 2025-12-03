"""
Atlas4D Python SDK

Simple client for Atlas4D spatiotemporal platform.

Example:
    >>> from atlas4d import Client
    >>> client = Client()
    >>> 
    >>> # Ask documentation questions
    >>> answer = client.ask("How do I create a module?")
    >>> print(answer.text)
    >>> 
    >>> # Get observations
    >>> obs = client.observations.list(limit=10)
"""

from .client import Client, RAGAnswer

__version__ = "0.2.0"
__all__ = ["Client", "RAGAnswer"]
