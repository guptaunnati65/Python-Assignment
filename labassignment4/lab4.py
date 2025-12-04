import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ========== FOLDER SETUP ==========
OUTPUT_FOLDER = "outputs"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ========== TASK 1: DATA LOADING ==========
file_path = "weather_forecast_data.csv"

df = pd.read_csv(file_path)

print("\n--- HEAD ---")
print(df.head())

print("\n--- INFO ---")
print(df.info())

print("\n--- DESCRIBE ---")
print(df.describe(include="all"))

# ========== TASK 2: DATA CLEANING ==========

# Convert date column to datetime (common column names checked)
date_columns = ["date", "Date", "DATE", "day"]
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        df.rename(columns={col: "Date"}, inplace=True)
        break

# Drop rows where date is missing
df = df.dropna(subset=["Date"])

# Fill numeric missing values with median
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Optional: rename common columns if found
rename_map = {
    "temp": "Temperature",
    "temperature": "Temperature",
    "humidity": "Humidity",
    "rain": "Rainfall",
    "rainfall": "Rainfall"
}
df.rename(columns={col: rename_map[col] for col in df.columns if col.lower() in rename_map}, inplace=True)

# Save cleaned data
df.to_csv(f"{OUTPUT_FOLDER}/cleaned_data.csv", index=False)

# ========== TASK 3: STATISTICAL ANALYSIS ==========
print("\n--- NUMPY STATISTICS ---")

stats = {}

for col in ["Temperature", "Humidity", "Rainfall"]:
    if col in df.columns:
        stats[col] = {
            "mean": np.mean(df[col]),
            "min": np.min(df[col]),
            "max": np.max(df[col]),
            "std": np.std(df[col])
        }

        print(f"\n{col} Stats:")
        for k, v in stats[col].items():
            print(f"{k}: {v}")

# ========== TASK 4: VISUALIZATION ==========

# --- Line chart: Daily temperature trend ---
if "Temperature" in df.columns:
    plt.figure(figsize=(12, 5))
    plt.plot(df["Date"], df["Temperature"])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.grid(True)
    plt.savefig(f"{OUTPUT_FOLDER}/temperature_trend.png")
    plt.close()

# --- Bar chart: Monthly Rainfall ---
if "Rainfall" in df.columns:
    monthly_rain = df.groupby(df["Date"].dt.month)["Rainfall"].sum()

    plt.figure(figsize=(10, 5))
    monthly_rain.plot(kind="bar")
    plt.title("Monthly Rainfall Total")
    plt.xlabel("Month")
    plt.ylabel("Rainfall")
    plt.savefig(f"{OUTPUT_FOLDER}/monthly_rainfall.png")
    plt.close()

# --- Scatter plot: Humidity vs Temperature ---
if "Temperature" in df.columns and "Humidity" in df.columns:
    plt.figure(figsize=(7, 5))
    plt.scatter(df["Temperature"], df["Humidity"])
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Humidity")
    plt.savefig(f"{OUTPUT_FOLDER}/humidity_vs_temperature.png")
    plt.close()

# --- Combined subplot example ---
if "Temperature" in df.columns and "Rainfall" in df.columns:
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    ax[0].plot(df["Date"], df["Temperature"], label="Temp")
    ax[0].set_title("Temperature Trend")

    ax[1].bar(df["Date"].dt.month, df["Rainfall"])
    ax[1].set_title("Rainfall by Month")

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_FOLDER}/combined_plot.png")
    plt.close()

# ========== TASK 5: GROUPING ==========

df["Month"] = df["Date"].dt.month

monthly_stats = df.groupby("Month")[["Temperature", "Humidity", "Rainfall"]].mean()
monthly_stats.to_csv(f"{OUTPUT_FOLDER}/monthly_stats.csv")

print("\nMonthly Statistics Saved!")

# ========== FINAL MESSAGE ==========
print("\nAll tasks completed successfully!")
print("Outputs are saved inside the 'outputs' folder.")