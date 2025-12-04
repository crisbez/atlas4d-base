# Changelog

All notable changes to the `atlas4d` Python SDK will be documented in this file.

## [0.3.0] - 2025-12-04

### Added
- `AsyncClient` with full async support using httpx
- Async versions of all API methods (`ask()`, `observations.list()`, etc.)

### Changed
- Bumped minimum Python version to 3.9+
- Added `httpx>=0.24.0` as dependency

## [0.2.0] - 2025-12-03

### Added
- `Client.ask()` method for RAG documentation queries
- `RAGAnswer` dataclass with text, sources, chunks_used
- `Client.rag.query()` for full RAG API access
- Support for English and Bulgarian responses

## [0.1.0] - 2025-12-03

### Added
- Initial `Client` implementation
- `health()` and `stats()` methods
- `observations.list()` and `observations.geojson()`
- `anomalies.list()`
- Environment variable configuration (ATLAS4D_HOST, ATLAS4D_PORT)
- Context manager support
