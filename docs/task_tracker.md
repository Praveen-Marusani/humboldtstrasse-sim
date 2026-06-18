# Project Task Tracker

Track progress here. Update status as you go.

## Phase 1 – Setup (Week 1)
- [ ] Create GitHub repo and invite all group members
- [ ] Install AnyLogic Personal Learning Edition
- [ ] Download OSM data for intersection area
- [ ] Download city planning PDF (roundabout design)
- [ ] Read project description and agree on research questions

## Phase 2 – Data Collection (Week 1–2)
- [ ] Schedule on-site traffic count session (aim for morning peak 7:30–8:30)
- [ ] Count vehicles, cyclists, pedestrians per arm
- [ ] Optional: video record intersection for later analysis
- [ ] Fill in `data/raw/traffic_counts_template.csv`
- [ ] Run `scripts/process_traffic_counts.py` to get arrival rates

## Phase 3 – Model Building (Week 2–3)
- [ ] Build road network SC-A in AnyLogic (GIS background + road elements)
- [ ] Add Car agents with correct parameters
- [ ] Add Pedestrian and Cyclist agents
- [ ] Add traffic sources with measured arrival rates
- [ ] Add KPI collection (travel time, queue, conflicts, CO2 proxy)
- [ ] Verify model: mass balance, animation check
- [ ] Clone SC-A → create SC-B (modify intersection to roundabout)

## Phase 4 – Experiments (Week 3–4)
- [ ] Experiment 1: Baseline validation (SC-A vs observations)
- [ ] Experiment 2: SC-A vs SC-B comparison (10 replications)
- [ ] Experiment 3: Sensitivity analysis (vary demand 50–150%)
- [ ] Experiment 4: Time-varying demand (peak hour profile)
- [ ] Export results CSVs
- [ ] Run `scripts/plot_results.py` to generate figures

## Phase 5 – Report Writing (Week 4–5)
- [ ] Introduction (1 person)
- [ ] Literature review – 5 papers summarized (1–2 people)
- [ ] Methodology section (1 person)
- [ ] Implementation section with screenshots (1 person)
- [ ] Results & evaluation section with figures (1–2 people)
- [ ] Discussion, limitations, improvements (all)
- [ ] Summary and references (1 person)
- [ ] Proofread and format final PDF

## Deadlines
| Task | Deadline |
|------|----------|
| Model complete + experiments done | ~28 June 2026 |
| Report draft ready for review | ~1 July 2026 |
| **Report submitted (Moodle)** | **5 July 2026, 23:59 CEST** |
| **Presentation** | **8 July 2026** |
