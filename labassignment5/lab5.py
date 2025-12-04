import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime



DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

DATASET_FILE = "green_smart_campus_dataset.csv"   




def load_all_csv(data_folder):
    files = list(Path(data_folder).glob("*.csv"))
    if not files:
        raise FileNotFoundError("No CSV files found in /data/ folder.")

    merged_df = pd.DataFrame()
    log = []

    for file in files:
        try:
            df = pd.read_csv(file, on_bad_lines="skip")
            df["building"] = file.stem  
            merged_df = pd.concat([merged_df, df], ignore_index=True)

        except Exception as e:
            log.append(f"Error loading {file}: {e}")

    print("\nData Loading Issues:", log)
    return merged_df



if not os.path.exists(f"{DATA_FOLDER}/{DATASET_FILE}"):
    import shutil
    shutil.copy(DATASET_FILE, f"{DATA_FOLDER}/{DATASET_FILE}")

df = load_all_csv(DATA_FOLDER)


df.columns = [c.lower() for c in df.columns]


if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")


df.fillna(df.median(numeric_only=True), inplace=True)

print("\nMerged Dataset Preview:")
print(df.head())


df.to_csv(f"{OUTPUT_FOLDER}/cleaned_energy_data.csv", index=False)




def calculate_daily_totals(df):
    return df.resample("D", on="timestamp")["kwh"].sum()

def calculate_weekly_totals(df):
    return df.resample("W", on="timestamp")["kwh"].sum()

def building_wise_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])


daily_totals = calculate_daily_totals(df)
weekly_totals = calculate_weekly_totals(df)
building_summary = building_wise_summary(df)

building_summary.to_csv(f"{OUTPUT_FOLDER}/building_summary.csv")




class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        return {
            "building": self.name,
            "total_kwh": self.calculate_total_consumption(),
            "readings_count": len(self.meter_readings)
        }


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def load_from_dataframe(self, df):
        for _, row in df.iterrows():
            b = row["building"]
            if b not in self.buildings:
                self.buildings[b] = Building(b)
            reading = MeterReading(row["timestamp"], row["kwh"])
            self.buildings[b].add_reading(reading)

    def generate_all_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


manager = BuildingManager()
manager.load_from_dataframe(df)
reports = manager.generate_all_reports()




plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots(1, 3, figsize=(18, 5))


ax[0].plot(daily_totals.index, daily_totals.values)
ax[0].set_title("Daily Consumption Trend")
ax[0].set_xlabel("Date")
ax[0].set_ylabel("kWh")

ax[1].bar(weekly_totals.index.astype(str), weekly_totals.values)
ax[1].set_title("Weekly Consumption Totals")
ax[1].set_xticklabels([], rotation=90)

g
sample_df = df.copy()
sample_df["hour"] = sample_df["timestamp"].dt.hour
ax[2].scatter(sample_df["hour"], sample_df["kwh"], alpha=0.5)
ax[2].set_title("Peak Hour Consumption Distribution")
ax[2].set_xlabel("Hour of Day")
ax[2].set_ylabel("kWh")

plt.tight_layout()
plt.savefig(f"{OUTPUT_FOLDER}/dashboard.png")
plt.close()




total_consumption = df["kwh"].sum()
highest_building = building_summary["sum"].idxmax()
peak_load_time = df.groupby(df["timestamp"].dt.hour)["kwh"].sum().idxmax()

summary_text = f"""
CAMPUS ENERGY SUMMARY REPORT
----------------------------

Total Energy Consumption: {total_consumption:.2f} kWh

Highest Consuming Building: {highest_building}

Peak Load Hour: {peak_load_time}:00 hrs

Daily Trend: Data saved in daily_totals.csv
Weekly Trend: Data saved in weekly_totals.csv

Dashboard Image: dashboard.png
"""

with open(f"{OUTPUT_FOLDER}/summary.txt", "w") as f:
    f.write(summary_text)

print("\nSUMMARY REPORT GENERATED!\n")
print(summary_text)
