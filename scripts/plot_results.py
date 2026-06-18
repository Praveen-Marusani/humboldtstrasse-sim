"""
plot_results.py
Reads AnyLogic exported result CSVs and produces comparison charts for the report.

Usage:
    python scripts/plot_results.py

Expected input files (export from AnyLogic after running experiments):
    results/tables/SC_A_results.csv
    results/tables/SC_B_results.csv

Output:
    results/figures/travel_time_comparison.png
    results/figures/queue_length_comparison.png
    results/figures/conflict_events_comparison.png
    results/figures/co2_proxy_comparison.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.rcParams["figure.dpi"] = 150
matplotlib.rcParams["font.family"] = "sans-serif"

RESULTS_DIR = "results/tables"
FIGURES_DIR = "results/figures"

SCENARIO_A_FILE = os.path.join(RESULTS_DIR, "SC_A_results.csv")
SCENARIO_B_FILE = os.path.join(RESULTS_DIR, "SC_B_results.csv")


def load_results():
    """Load scenario result CSVs exported from AnyLogic."""
    if not os.path.exists(SCENARIO_A_FILE) or not os.path.exists(SCENARIO_B_FILE):
        print("Result files not found. Generating example data for testing.")
        return generate_example_data()
    sc_a = pd.read_csv(SCENARIO_A_FILE)
    sc_b = pd.read_csv(SCENARIO_B_FILE)
    return sc_a, sc_b


def generate_example_data():
    """Placeholder data — replace with real AnyLogic exports."""
    import numpy as np
    np.random.seed(42)
    n = 10  # replications

    sc_a = pd.DataFrame({
        "Replication": range(1, n+1),
        "AvgTravelTime_s": np.random.normal(45, 5, n),
        "MaxQueueLength_veh": np.random.normal(8, 2, n),
        "ConflictEvents": np.random.randint(12, 25, n),
        "CO2_Proxy_kg": np.random.normal(3.2, 0.4, n),
    })
    sc_b = pd.DataFrame({
        "Replication": range(1, n+1),
        "AvgTravelTime_s": np.random.normal(32, 4, n),
        "MaxQueueLength_veh": np.random.normal(4, 1.5, n),
        "ConflictEvents": np.random.randint(4, 12, n),
        "CO2_Proxy_kg": np.random.normal(2.1, 0.3, n),
    })
    return sc_a, sc_b


def bar_comparison(metric, label, unit, sc_a, sc_b, filename):
    """Bar chart comparing mean ± std for one metric across both scenarios."""
    means = [sc_a[metric].mean(), sc_b[metric].mean()]
    stds = [sc_a[metric].std(), sc_b[metric].std()]
    colors = ["#E07B39", "#3A7EBF"]  # orange for current, blue for roundabout

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(["SC-A: Current\nIntersection", "SC-B: Planned\nRoundabout"],
                  means, yerr=stds, capsize=6, color=colors, alpha=0.85, edgecolor="black")
    ax.set_ylabel(f"{label} [{unit}]")
    ax.set_title(f"{label}: SC-A vs SC-B\n(mean ± std, n={len(sc_a)} replications)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Annotate bars
    for bar, mean, std in zip(bars, means, stds):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + std + 0.3,
                f"{mean:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved: {path}")


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    sc_a, sc_b = load_results()

    bar_comparison("AvgTravelTime_s", "Average Travel Time", "s",
                   sc_a, sc_b, "travel_time_comparison.png")

    bar_comparison("MaxQueueLength_veh", "Max Queue Length", "vehicles",
                   sc_a, sc_b, "queue_length_comparison.png")

    bar_comparison("ConflictEvents", "Conflict Events", "count",
                   sc_a, sc_b, "conflict_events_comparison.png")

    bar_comparison("CO2_Proxy_kg", "CO₂ Proxy (idling)", "kg",
                   sc_a, sc_b, "co2_proxy_comparison.png")

    # Summary table
    summary = pd.DataFrame({
        "Metric": ["Avg Travel Time (s)", "Max Queue (veh)", "Conflicts", "CO₂ Proxy (kg)"],
        "SC-A Mean": [sc_a["AvgTravelTime_s"].mean(), sc_a["MaxQueueLength_veh"].mean(),
                      sc_a["ConflictEvents"].mean(), sc_a["CO2_Proxy_kg"].mean()],
        "SC-A Std": [sc_a["AvgTravelTime_s"].std(), sc_a["MaxQueueLength_veh"].std(),
                     sc_a["ConflictEvents"].std(), sc_a["CO2_Proxy_kg"].std()],
        "SC-B Mean": [sc_b["AvgTravelTime_s"].mean(), sc_b["MaxQueueLength_veh"].mean(),
                      sc_b["ConflictEvents"].mean(), sc_b["CO2_Proxy_kg"].mean()],
        "SC-B Std": [sc_b["AvgTravelTime_s"].std(), sc_b["MaxQueueLength_veh"].std(),
                     sc_b["ConflictEvents"].std(), sc_b["CO2_Proxy_kg"].std()],
    })
    summary["Change_%"] = ((summary["SC-B Mean"] - summary["SC-A Mean"]) / summary["SC-A Mean"] * 100).round(1)
    out = os.path.join(RESULTS_DIR, "summary_comparison.csv")
    summary.to_csv(out, index=False)
    print(f"\nSummary table saved: {out}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
