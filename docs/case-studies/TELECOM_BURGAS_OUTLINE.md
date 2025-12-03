# Case Study: Telecom Network Monitoring in Burgas Region

**Status:** Outline (Draft)  
**Industry:** Telecommunications  
**Location:** Burgas, Bulgaria  
**Platform:** Atlas4D with Network Guardian Module

---

## 1. Context

### Operator Profile
- Regional ISP serving Burgas and surrounding area
- ~50,000 subscribers (residential + business)
- Mix of GPON fiber, wireless, and legacy DSL

### Network Footprint
- **3 OLT nodes** - Central, North, South distribution
- **5 aggregation switches** - Layer 2/3 core
- **20+ CPE devices** - Customer premises equipment
- **~200km fiber** - GPON infrastructure

### Existing Tools (Before Atlas4D)
- Cacti for SNMP polling
- Nagios for alerting
- Excel spreadsheets for capacity planning
- Manual log correlation

---

## 2. Challenges

### Fragmented Monitoring
- **Problem:** 4 different tools, no unified view
- **Impact:** 30+ minutes to correlate events across systems
- **Example:** OLT alarm + switch log + customer ticket = manual work

### No Spatiotemporal View
- **Problem:** Can't see network health geographically over time
- **Impact:** Outages in specific areas not detected until customer calls
- **Example:** Fiber cut affecting 3 streets - discovered after 2 hours

### Manual Event Correlation
- **Problem:** Engineers manually connect dots between events
- **Impact:** High MTTR (Mean Time to Resolve)
- **Example:** Power fluctuation → OLT restart → 50 customers offline

### Capacity Blindness
- **Problem:** No predictive view of network capacity
- **Impact:** Reactive upgrades, customer complaints
- **Example:** Evening congestion discovered only via complaints

---

## 3. Atlas4D Setup

### Data Sources Integrated

| Source | Protocol | Frequency | Data Type |
|--------|----------|-----------|-----------|
| OLT devices | SNMP v2c | 5 min | Ports, power, traffic |
| Switches | SNMP v2c | 5 min | Interface stats |
| CPE | TR-069 | 15 min | Signal, errors |
| Weather | REST API | 1 hour | Temp, wind, rain |

### Atlas4D Components Used
```
Atlas4D Stack
├── Core (PostgreSQL + PostGIS + TimescaleDB)
├── Network Guardian Module
│   ├── SNMP collector
│   ├── Device topology
│   └── Alert rules
├── NLQ Service (Bulgarian queries)
└── Grafana Dashboards
```

### Deployment Model
- **Server:** On-premises (customer datacenter)
- **Resources:** 8 vCPU, 32GB RAM, 500GB NVMe
- **GPU:** None (CPU inference for NLQ)

### Key Configurations
- 90-day data retention (hypertables)
- 5-minute polling interval
- Geospatial indexing (H3 resolution 9)
- Bulgarian NLQ enabled

---

## 4. Results

### Mean Time to Detect (MTTD)
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| OLT issues | 15 min | 2 min | **87%** |
| Fiber cuts | 120 min | 10 min | **92%** |
| Congestion | 60 min | 5 min | **92%** |

### False Positive Reduction
- **Before:** ~20 alerts/day requiring investigation
- **After:** ~5 alerts/day (75% reduction)
- **Reason:** Correlation rules + anomaly detection

### Operator Efficiency
- **Query time:** 30 min manual → 10 sec NLQ
- **Report generation:** 2 hours → 5 minutes
- **Capacity planning:** Monthly → Real-time

### Example NLQ Queries in Production
```
Bulgarian:
"Покажи всички OLT с проблеми през последния час"
"Кои клиенти са засегнати от аварията в Сарафово?"
"Сравни трафика тази седмица с миналата"

English:
"Show devices with packet loss > 1% today"
"Which OLT has the highest utilization?"
"List anomalies in the last 24 hours"
```

### Sample Dashboard Metrics
- Network availability: 99.7% → 99.95%
- Customer tickets (network): -40%
- Engineer response time: -60%

---

## 5. Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                      Network Devices                         │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐               │
│  │OLT-1│  │OLT-2│  │OLT-3│  │SW-1 │  │SW-2 │  ...          │
│  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘               │
└─────┼────────┼────────┼────────┼────────┼───────────────────┘
      │ SNMP   │        │        │        │
      ▼        ▼        ▼        ▼        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Atlas4D Platform                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ SNMP Worker  │  │ Ping Worker  │  │Weather Worker│       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│         ▼                 ▼                 ▼                │
│  ┌────────────────────────────────────────────────────┐     │
│  │              PostgreSQL + Extensions                │     │
│  │   PostGIS │ TimescaleDB │ pgvector │ H3            │     │
│  └────────────────────────────────────────────────────┘     │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  NLQ Service │  │ API Gateway  │  │   Frontend   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
         │                   │                  │
         ▼                   ▼                  ▼
    Operators           Dashboards         Mobile App
```

---

## 6. Lessons Learned

### What Worked Well
- Bulgarian NLQ - operators adopted quickly
- Geospatial correlation - "see the network on a map"
- TimescaleDB compression - 10x storage savings

### Challenges Encountered
- Legacy SNMP devices - inconsistent MIBs
- Initial data quality - required cleanup
- Training - 2 days for full adoption

### Recommendations
- Start with core devices (OLT, aggregation)
- Define alert thresholds with operations team
- Build NLQ queries for common questions first

---

## 7. Next Steps

### Phase 2 (Planned)
- [ ] Predictive maintenance using ML
- [ ] Integration with ticketing system
- [ ] Customer-facing status page
- [ ] Automated remediation for common issues

### Expansion Opportunities
- Add wireless backhaul monitoring
- Integrate smart city sensors
- Weather-correlated predictions

---

## 8. Quotes

> "Before Atlas4D, I spent 30 minutes every morning checking different systems. Now I ask one question and get the answer."
> — Network Operations Engineer

> "The map view changed everything. We can see problems before customers call."
> — NOC Manager

---

## Contact

For more information about this case study:
- **Email:** office@atlas4d.tech
- **Website:** https://atlas4d.tech

---

*Draft: December 2025*  
*For internal use and investor presentations*
