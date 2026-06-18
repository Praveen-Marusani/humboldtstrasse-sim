# humboldtstrasse-sim
# Traffic Simulation – Humboldtstraße / Cranachstraße, Weimar

**Module:** Simulation Methods in Engineering – SoSe 2026  
**Faculty:** Civil Engineering, Chair of Intelligent Technical Design  
**Bauhaus-Universität Weimar**

---

## Project Overview

This project models and compares two traffic scenarios at the intersection of **Humboldtstraße, Cranachstraße, Wilhelm-Külz-Straße, and Henßstraße** in Weimar:

| Scenario | Description |
|----------|-------------|
| **SC-A** | Current intersection (priority-based, no traffic signals) |
| **SC-B** | Planned roundabout (as per city planning documents) |

### Research Questions
1. Where do risky situations occur and who is involved? How can they be mitigated?
2. Can travel times and CO₂ emissions be reduced with the new roundabout?
3. What quantitative changes does the roundabout introduce?

---

## Repository Structure

```
humboldtstrasse-sim/
│
├── model/                        # AnyLogic project files
│   ├── SC_A_Intersection/        # Scenario A – current intersection
│   │   └── SC_A_Intersection.alp
│   └── SC_B_Roundabout/          # Scenario B – planned roundabout
│       └── SC_B_Roundabout.alp
│
├── data/
│   ├── raw/                      # Raw traffic counts, OSM exports, city docs
│   │   ├── traffic_counts.xlsx
│   │   ├── intersection_osm.geojson
│   │   └── roundabout_plan.pdf
│   └── processed/                # Cleaned input data used in AnyLogic
│       ├── arrival_rates_SC_A.csv
│       └── arrival_rates_SC_B.csv
│
├── scripts/                      # Helper scripts (Python/R) for data processing
│   ├── process_traffic_counts.py
│   └── plot_results.py
│
├── results/
│   ├── figures/                  # Output charts and visualizations
│   └── tables/                   # Summary statistics (CSV/Excel)
│
├── docs/                         # Reference documents and literature notes
│   └── literature_notes.md
│
├── report/                       # Final report files
│   └── report.pdf                # Submitted after completion
│
├── .gitignore
└── README.md
```

---

## Deliverables

| Deliverable | Deadline | Format |
|-------------|----------|--------|
| Group Report | **5 July 2026, 23:59 CEST** | PDF via Moodle |
| AnyLogic Simulation | **5 July 2026, 23:59 CEST** | ZIP via Moodle |
| Presentation | **8 July 2026** | In-person |

---

## Model Parameters

### Input Parameters
| Parameter | SC-A | SC-B | Unit |
|-----------|------|------|------|
| Vehicle arrival rate (Humboldtstr.) | TBD | TBD | veh/h |
| Vehicle arrival rate (Cranachstr.) | TBD | TBD | veh/h |
| Vehicle arrival rate (Wilhelm-Külz-Str.) | TBD | TBD | veh/h |
| Vehicle arrival rate (Henßstr.) | TBD | TBD | veh/h |
| Pedestrian arrival rate | TBD | TBD | ped/h |
| Cyclist arrival rate | TBD | TBD | cyc/h |
| Simulation duration | 3600 | 3600 | s |
| Number of replications | 10 | 10 | – |

### Output Parameters (KPIs)
- Average travel time through intersection (s)
- Maximum queue length per arm (vehicles)
- Number of conflict events (risk indicator)
- Total vehicle delay (veh·s)
- Estimated CO₂ proxy (idling time × emission factor)

---

## AnyLogic Model Structure

### Agents
- **`Car`** – standard vehicle agent with speed, origin, destination
- **`Cyclist`** – slower agent, uses bike lanes/shared space
- **`Pedestrian`** – uses crosswalks, interacts with vehicles

### Main Components (SC-A – Intersection)
- `RoadNetwork` – OSM-imported road geometry
- `TrafficSource` per arm – Poisson arrival process
- `IntersectionControl` – priority rules (right-before-left / yield signs)
- `ConflictDetector` – logs agent proximity events as risk indicators
- `KPI_Dashboard` – real-time plots of travel time, queue length

### Main Components (SC-B – Roundabout)
- Same agents, modified `RoadNetwork` with circular geometry
- `RoundaboutYield` – give-way logic for entering vehicles
- Same KPI tracking for direct comparison

---

## How to Open the Model

1. Install **AnyLogic Personal Learning Edition** (free): https://www.anylogic.com/downloads/
2. Open `model/SC_A_Intersection/SC_A_Intersection.alp` or `SC_B_Roundabout/SC_B_Roundabout.alp`
3. Click **Run** to start the simulation
4. Adjust arrival rates in the **Parameters** panel before running

---

## Data Sources

- OpenStreetMap: https://www.openstreetmap.org/#map=19/50.973742/11.322184
- City of Weimar planning documents: https://stadt.weimar.de/de/bauvorhaben/gemeinschaftsmassnahme-ausbau-der-humboldtstrasse-von-der-cranachstrasse-bis-zur-theodor-koerner-strasse-in-weimar.html
- Roundabout plan PDF: https://stadt.weimar.de/de/datei/anzeigen/id/85679,48/projektvorstellung_humboldtstra_e.pdf
- Manual traffic counts (collected by group)

---

## Team & Contributions

| Member | Tasks |
|--------|-------|
| TBD | System analysis, model design |
| TBD | AnyLogic implementation SC-A |
| TBD | AnyLogic implementation SC-B |
| TBD | Data collection & processing |
| TBD | Report writing, results analysis |

---

## Literature

See `docs/literature_notes.md` for summaries of referenced papers.
