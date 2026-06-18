"""
process_traffic_counts.py
Converts raw traffic count CSV into arrival rate tables for AnyLogic.

Usage:
    python scripts/process_traffic_counts.py

Output:
    data/processed/arrival_rates_SC_A.csv
    data/processed/arrival_rates_SC_B.csv
"""

import pandas as pd
import os

RAW_FILE = "data/raw/traffic_counts_template.csv"
OUT_DIR = "data/processed"


def load_counts(filepath):
    df = pd.read_csv(filepath)
    # Drop placeholder rows (no count value)
    df = df.dropna(subset=["Count"])
    df["Count"] = pd.to_numeric(df["Count"], errors="coerce")
    df = df.dropna(subset=["Count"])
    return df


def compute_arrival_rates(df):
    """
    Converts hourly counts to arrival rates (vehicles/second) per arm and agent type.
    AnyLogic Road Traffic library expects arrivals per hour or inter-arrival time in seconds.
    """
    # Group by time period, arm, and agent type
    summary = (
        df.groupby(["Time_Start", "Road_Arm", "Agent_Type"])["Count"]
        .sum()
        .reset_index()
    )
    summary["Arrivals_per_hour"] = summary["Count"]
    summary["Interarrival_seconds"] = 3600.0 / summary["Arrivals_per_hour"]
    return summary


def save_scenario(df, time_start, filename):
    period = df[df["Time_Start"] == time_start].copy()
    out_path = os.path.join(OUT_DIR, filename)
    period.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
    return period


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("Loading raw traffic counts...")
    df = load_counts(RAW_FILE)

    print("Computing arrival rates...")
    rates = compute_arrival_rates(df)

    # Print summary
    print("\n--- Arrival Rate Summary ---")
    print(rates.to_string(index=False))

    # Save one file per scenario (SC-A and SC-B share the same measured input;
    # SC-B geometry is different but demand is the same — adjust here if needed)
    rates.to_csv(os.path.join(OUT_DIR, "arrival_rates_SC_A.csv"), index=False)
    rates.to_csv(os.path.join(OUT_DIR, "arrival_rates_SC_B.csv"), index=False)

    print("\nDone. Files saved to data/processed/")
    print("Import these CSVs into AnyLogic as dataset parameters.")


if __name__ == "__main__":
    main()
