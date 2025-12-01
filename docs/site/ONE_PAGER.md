# Atlas4D - Open 4D Spatiotemporal Platform

## 🎯 One Line

**Unified PostgreSQL stack for space + time + ML - query your 4D world in plain language.**

---

## 🔥 The Problem

Building spatiotemporal applications today means:
- Geographic data in PostGIS
- Time-series in InfluxDB/TimescaleDB
- ML embeddings in Pinecone/pgvector
- 4-5 databases, complex ETL, no unified queries

**Result:** Months to build, hard to maintain, impossible to ask simple questions.

---

## 💡 Our Solution

Atlas4D unifies everything in PostgreSQL:
```
PostgreSQL 16
├── PostGIS      → Where (spatial)
├── TimescaleDB  → When (time-series)
├── pgvector     → What it means (ML)
└── JSONB        → Everything else
```

**One database. One query. One answer.**

---

## ✨ Key Features

| Feature | What It Does |
|---------|--------------|
| **Natural Language Queries** | Ask in Bulgarian or English: "Покажи заплахи в София" |
| **Multi-Domain** | Same engine for telecom, mobility, defense, smart city |
| **ML-Ready** | Trajectory embeddings, anomaly detection built-in |
| **Observable** | Prometheus + Grafana from day one |
| **Open Core** | Apache 2.0 base, enterprise modules available |

---

## 👥 Who It's For

- **Telecom teams** monitoring network infrastructure
- **Smart city projects** tracking mobility and sensors
- **Defense organizations** correlating multi-source intelligence
- **Data engineers** tired of managing 5 databases

---

## 🚀 Try It Now
```bash
git clone https://github.com/crisbez/atlas4d-base
cd atlas4d-base
docker compose up -d
# Open http://localhost:8091
```

**Time to first map: 5 minutes**

---

## 📊 By The Numbers

| Metric | Value |
|--------|-------|
| Setup time | < 5 minutes |
| Query speedup (cached) | 150x |
| Docker image (optimized) | 758 MB |
| Demo scenarios | 2 (Mobility + Telecom) |

---

## 🏢 About

Built by **Digicom Ltd** (Bulgaria) - technology company focused on spatiotemporal intelligence.

**Contact:** office@atlas4d.tech  
**GitHub:** github.com/crisbez/atlas4d-base

---

*"The Linux of 4D spatiotemporal platforms"*
