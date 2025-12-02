# Atlas4D Demo Video Script

**Duration:** 3-4 minutes  
**Title:** "Atlas4D Base v0.3.0 – From Zero to Map in 5 Minutes"  
**Style:** Screen recording with voice-over (or text overlays)

---

## Pre-Recording Checklist

- [ ] Clean terminal (clear history, large font)
- [ ] Browser ready (empty tabs, bookmarks hidden)
- [ ] Docker running, no other containers
- [ ] atlas4d-base folder deleted (fresh start)

---

## Script

### Scene 1: Title (0:00 - 0:05)
**Screen:** Title card
```
Atlas4D Base v0.3.0
Open 4D Spatiotemporal Platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
github.com/crisbez/atlas4d-base
```

### Scene 2: Introduction (0:05 - 0:15)
**Voice/Text:** 
> "Atlas4D unifies spatial, time-series, and ML data in one PostgreSQL stack. Let's go from zero to working map in under 5 minutes."

### Scene 3: Clone Repository (0:15 - 0:30)
**Terminal:**
```bash
git clone https://github.com/crisbez/atlas4d-base
cd atlas4d-base
ls -la
```
**Voice/Text:**
> "Clone the repo. You'll see docker-compose, SQL schemas, and services."

### Scene 4: Start Stack (0:30 - 1:00)
**Terminal:**
```bash
docker compose up -d
```
**Voice/Text:**
> "One command starts PostgreSQL with PostGIS, TimescaleDB, pgvector, plus Redis, API gateway, and frontend."

**Show:** Wait for containers to start
```bash
docker compose ps
```

### Scene 5: Health Check (1:00 - 1:15)
**Terminal:**
```bash
curl http://localhost:8090/health | jq
```
**Voice/Text:**
> "Health endpoint confirms all services are running."

### Scene 6: Load Demo Data (1:15 - 1:35)
**Terminal:**
```bash
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f /docker-entrypoint-initdb.d/seed/demo_burgas.sql
```
**Voice/Text:**
> "Load the Burgas mobility demo - 500 observations, 30 anomalies, 3 source types."

### Scene 7: Check Stats (1:35 - 1:50)
**Terminal:**
```bash
curl http://localhost:8090/api/stats | jq
```
**Voice/Text:**
> "API confirms our data is loaded."

### Scene 8: Open Map - Mobility (1:50 - 2:20)
**Browser:** Navigate to http://localhost:8091
**Voice/Text:**
> "Open the map. We see vehicle, sensor, and camera observations around Burgas, Bulgaria."

**Actions:**
- Click on a few markers to show popups
- Show the legend
- Point out different colors for source types

### Scene 9: Load Telecom Demo (2:20 - 2:40)
**Terminal:**
```bash
docker compose exec postgres psql -U atlas4d_app -d atlas4d \
  -f /docker-entrypoint-initdb.d/seed/demo_telecom.sql
```
**Voice/Text:**
> "Now let's add a telecom scenario - OLT nodes, switches, and CPE devices."

### Scene 10: Switch to Telecom (2:40 - 3:10)
**Browser:** 
- Refresh map
- Select "📡 Telecom" from dropdown

**Voice/Text:**
> "Same platform, different domain. The scenario toggle switches between mobility and network infrastructure."

**Actions:**
- Click on OLT node (show capacity, ports)
- Click on CPE (show power levels)
- Point out anomalies

### Scene 11: API Examples (3:10 - 3:30)
**Terminal:**
```bash
# Get observations
curl "http://localhost:8090/api/observations?limit=3" | jq

# Get anomalies
curl "http://localhost:8090/api/anomalies" | jq '.[0]'
```
**Voice/Text:**
> "Full REST API for integration. Query observations, anomalies, get GeoJSON for mapping."

### Scene 12: Closing (3:30 - 3:50)
**Screen:** End card
```
Atlas4D Base v0.3.0
━━━━━━━━━━━━━━━━━━━━
⭐ Star: github.com/crisbez/atlas4d-base
📖 Docs: Quick Start Guide
📧 Contact: office@atlas4d.tech
━━━━━━━━━━━━━━━━━━━━
PostgreSQL │ PostGIS │ TimescaleDB │ pgvector
```

**Voice/Text:**
> "That's Atlas4D Base - open 4D spatiotemporal platform. Star the repo, try the Quick Start, and let us know what you build!"

---

## Post-Recording

### Video Description (YouTube)
```
Atlas4D Base v0.3.0 – Quick Start Demo

Open 4D Spatiotemporal AI Platform built on PostgreSQL.
From zero to working map in under 5 minutes.

🔗 Links:
━━━━━━━━
⭐ GitHub: https://github.com/crisbez/atlas4d-base
📖 Quick Start: https://github.com/crisbez/atlas4d-base/blob/main/docs/quickstart/QUICK_START.md
📰 Blog: "Why We Built Atlas4D"
📧 Contact: office@atlas4d.tech

📦 Stack:
━━━━━━━━
- PostgreSQL 16
- PostGIS 3.4
- TimescaleDB
- pgvector
- Redis
- FastAPI

🏷️ Tags:
#postgresql #postgis #timescaledb #pgvector #geospatial #spatiotemporal #opensource #docker #fastapi
```

### Thumbnail Ideas
- Screenshot of map with "Atlas4D v0.3.0" overlay
- Split screen: Terminal + Map
- "Zero to Map in 5 min" text

---

## Recording Tips

1. **Terminal:**
   - Font size: 18-20pt
   - Clean prompt: `$` or `atlas4d $`
   - Dark theme

2. **Browser:**
   - Hide bookmarks bar
   - Zoom to 100-125%
   - Close other tabs

3. **Recording:**
   - 1920x1080 resolution
   - OBS or similar
   - Record audio separately if needed

4. **Editing:**
   - Speed up docker pull/build (2-4x)
   - Add text overlays for key moments
   - Add subtle background music (optional)

---

*Prepared for Sprint 23, Story 2*
