# AnyLogic Model Design Specification

## Overview

Two models are built in AnyLogic using the **Road Traffic Library**:

| Model | File | Description |
|-------|------|-------------|
| SC-A | `model/SC_A_Intersection/SC_A_Intersection.alp` | Current priority intersection |
| SC-B | `model/SC_B_Roundabout/SC_B_Roundabout.alp` | Planned roundabout |

---

## 1. Road Network Setup

### How to build the network in AnyLogic:

1. Open AnyLogic → New Model → select **Road Traffic Library**
2. In the diagram, add a **Road Network** element
3. Use **GIS Map** background:
   - Go to `Space Markup` → enable GIS map
   - Center on: `50.9737, 11.3222` (Humboldtstraße/Cranachstraße)
   - Zoom to level 18
4. Draw roads using **Road** elements tracing the 4 streets:
   - Humboldtstraße (N–S axis)
   - Cranachstraße (E–W)
   - Wilhelm-Külz-Straße (SW approach)
   - Henßstraße (NW approach)
5. Add **Intersection** element at center for SC-A, or **Roundabout** element for SC-B

### SC-A Intersection Control:
- Set intersection type: **Uncontrolled** (right-before-left rule, Germany)
- Or add **Stop/Yield** signs on minor arms if applicable
- Add **Crosswalk** elements at pedestrian crossing points

### SC-B Roundabout Control:
- Replace center intersection with **Roundabout** element
- Set inner radius: ~15m (from city plan)
- Set yield rule: entering traffic yields to circulating traffic

---

## 2. Agents

### Car Agent
```
Agent type: Car (built-in Road Traffic)
Parameters:
  - maxSpeed: triangular(30, 50, 60) km/h   [within intersection zone]
  - acceleration: 2.5 m/s²
  - deceleration: 4.5 m/s²
  - length: triangular(3.5, 4.5, 5.5) m
Tracking:
  - entryTime: double   [set when entering network]
  - exitTime: double    [set when leaving]
  - travelTime: exitTime - entryTime
```

### Cyclist Agent (custom agent)
```
Agent type: Pedestrian (Road Traffic) or custom
Parameters:
  - speed: triangular(10, 15, 20) km/h
  - uses dedicated bike lane if available, else road shoulder
Tracking:
  - entryTime, exitTime, travelTime
```

### Pedestrian Agent
```
Agent type: Pedestrian (Road Traffic Library)
Parameters:
  - speed: triangular(1.0, 1.4, 1.8) m/s
  - crosses at designated crosswalks only
Tracking:
  - waitTime at crosswalk
```

---

## 3. Traffic Sources

Add one **CarSource** (or **PedestrianSource**) per approach arm:

| Source Name | Road Arm | Agent Type | Arrival Rate |
|-------------|----------|------------|--------------|
| `src_Humboldt_N` | Humboldtstraße North | Car | from CSV parameter |
| `src_Humboldt_S` | Humboldtstraße South | Car | from CSV parameter |
| `src_Cranach_E` | Cranachstraße East | Car | from CSV parameter |
| `src_WKS` | Wilhelm-Külz-Straße | Car | from CSV parameter |
| `src_Henss` | Henßstraße | Car | from CSV parameter |
| `src_ped_*` | All arms | Pedestrian | from CSV parameter |
| `src_cyc_*` | All arms | Cyclist | from CSV parameter |

**Arrival distribution:** Poisson (exponential inter-arrival times)  
`interArrivalTime = exponential(3600.0 / arrivalsPerHour)`

---

## 4. Turn Movements (OD Matrix)

Define turning probabilities per source:

| From | Straight | Left | Right | U-turn |
|------|----------|------|-------|--------|
| Humboldt_N | 0.50 | 0.25 | 0.25 | 0.00 |
| Humboldt_S | 0.50 | 0.25 | 0.25 | 0.00 |
| Cranach_E | 0.40 | 0.30 | 0.30 | 0.00 |
| WKS | 0.60 | 0.20 | 0.20 | 0.00 |
| Henss | 0.60 | 0.20 | 0.20 | 0.00 |

*Adjust based on observed turning movements during traffic count.*

---

## 5. KPI Collection

### In AnyLogic, add to Main:

```java
// Variables (add as AnyLogic variables):
double totalTravelTime = 0;
int vehicleCount = 0;
int conflictCount = 0;
double totalIdleTime = 0;

// Datasets for charts:
DataSet ds_travelTime;      // histogram
DataSet ds_queueLength;     // time plot per arm
DataSet ds_conflicts;       // cumulative count
```

### On Car agent exit (add to CarSink `on agent removed`):
```java
double tt = agent.exitTime - agent.entryTime;
root.totalTravelTime += tt;
root.vehicleCount++;
root.ds_travelTime.add(tt);
```

### Conflict detection:
Use AnyLogic **Sensor** elements at conflict zones:
- When two agents of different types are within 5m → `conflictCount++`
- Log to `ds_conflicts`

### CO₂ proxy:
```java
// At each time step (use cyclic event, dt = 1s):
// If car speed < 5 km/h → idling
// CO2_idle_rate ≈ 0.0003 kg/s per vehicle (gasoline, ~1.2L/100km)
for (Car c : cars()) {
    if (c.speed() < 5.0 / 3.6) {
        totalIdleTime += 1.0;
    }
}
double co2Proxy = totalIdleTime * 0.0003;
```

---

## 6. Experiments

### Experiment 1 – Baseline Validation
- Run SC-A with measured peak-hour arrival rates
- Verify queue lengths match visual observations at intersection
- Check: travel times plausible for ~50m intersection crossing

### Experiment 2 – Scenario Comparison
- Run SC-A and SC-B with identical demand
- 10 replications each (to get statistical stability)
- Compare all 4 KPIs

### Experiment 3 – Sensitivity / Parametric Study
- Vary total demand: 50%, 75%, 100%, 125%, 150% of measured volume
- Observe how each scenario handles increasing load
- Plot KPIs vs demand level → find saturation point

### Experiment 4 – Peak Hour Profiles
- Run full simulation with time-varying demand (morning peak, midday, evening peak)
- Use AnyLogic **Schedule** element for time-varying arrival rates

---

## 7. Validation & Verification

### Verification (does the model do what we coded?)
- Check agent counts at sources vs sinks (mass balance)
- Inspect animation: no vehicles driving through walls
- Confirm yield/priority rules trigger correctly

### Validation (does the model match reality?)
- Compare simulated queue lengths to field observations
- Compare simulated travel times to manual measurements
- Document all validation checks in report Section 5

---

## 8. AnyLogic Export for Results

After running Monte Carlo experiment:
1. Right-click dataset → **Export to CSV**
2. Save to `results/tables/SC_A_results.csv` / `SC_B_results.csv`
3. Run `python scripts/plot_results.py` to generate figures

Columns needed in exported CSV:
```
Replication, AvgTravelTime_s, MaxQueueLength_veh, ConflictEvents, CO2_Proxy_kg
```
