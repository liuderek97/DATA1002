import pandas as pd
from pathlib import Path

ASSAULTS_CSV = r"C:\Users\olive\Desktop\DATA 1002\assaults_dow_timebins_2022_2024.csv"
VENUE_2022   = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2022.csv"
VENUE_2023   = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2023.csv"
VENUE_2024   = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2024.csv"
OUTDIR       = r"C:\Users\olive\Desktop\DATA 1002"

CBD_LGA_NAME = "Sydney"
CBD_AREA_KM2 = 1.651316939

outdir = Path(OUTDIR)
outdir.mkdir(parents=True, exist_ok=True)

# assaults: use the pre-filtered CSV (year/day/period/count)
a = pd.read_csv(ASSAULTS_CSV)
a = a[a["year"].isin([2022, 2023, 2024])].copy()

# night window = Fri/Sat/Sun 6pm-<12 + Sat/Sun/Mon 12am-<6
even  = a[(a["period"] == "6pm - < 12pm") & (a["day"].isin(["Friday","Saturday","Sunday"]))]
spill = a[(a["period"] == "12am - < 6am") & (a["day"].isin(["Saturday","Sunday","Monday"]))]
nw = pd.concat([even, spill], ignore_index=True).sort_values(["year","day","period"])
nw.to_csv(outdir / "assaults_night_window_2022_2024.csv", index=False)

yearly = nw.groupby("year", as_index=False)["count"].sum().rename(columns={"count":"total_night_window"})
yearly.to_csv(outdir / "assaults_night_window_yearly_totals.csv", index=False)

# venues: yearly metrics for Sydney
def load_venues(p, year):
    df = pd.read_csv(p)
    lga_col = next((c for c in df.columns if c.lower() in ("lga","lga_name") or "lga (2021)" in c.lower()), None)
    if lga_col:
        df = df[df[lga_col].astype(str).str.strip().str.lower() == CBD_LGA_NAME.lower()]
    df["year"] = year
    return df

v2022 = load_venues(VENUE_2022, 2022)
v2023 = load_venues(VENUE_2023, 2023)
v2024 = load_venues(VENUE_2024, 2024)
v = pd.concat([v2022, v2023, v2024], ignore_index=True)

# late_trading not used here; just overall venue counts + density
out_v = v.groupby("year", as_index=False).size().rename(columns={"size":"total_venues"})
out_v["late_venues"] = 0
out_v["late_share"] = 0.0
out_v["area_km2"] = CBD_AREA_KM2
out_v["density_km2"] = out_v["total_venues"] / CBD_AREA_KM2
out_v.to_csv(outdir / "venues_yearly_metrics.csv", index=False)

# merged table and simple extras
m = yearly.merge(out_v, on="year", how="left")
m["assaults_per_venue"] = m["total_night_window"] / m["total_venues"]
m.to_csv(outdir / "merged_panel_yearly.csv", index=False)
