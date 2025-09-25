# build_venues_late_density.py
import pandas as pd, numpy as np, re
from pathlib import Path

# edit paths if needed
VENUE_2022 = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2022.csv"
VENUE_2023 = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2023.csv"
VENUE_2024 = r"C:\Users\olive\Desktop\DATA 1002\filtered_premises_list_2024.csv"
ASSAULTS_NW = r"C:\Users\olive\Desktop\DATA 1002\assaults_night_window_2022_2024.csv"
ASSAULTS_YR = r"C:\Users\olive\Desktop\DATA 1002\assaults_night_window_yearly_totals.csv"
OUTDIR      = r"C:\Users\olive\Desktop\DATA 1002"

CBD_LGA_NAME = "Sydney"
CBD_AREA_KM2 = 1.651316939

TRUE_SET  = {"y","yes","true","1","t"}
FALSE_SET = {"n","no","false","0","f"}

def to_bool(x):
    if isinstance(x,(bool,np.bool_)): return bool(x)
    s = str(x).strip().lower()
    if s in TRUE_SET: return True
    if s in FALSE_SET: return False
    try: return float(s) != 0.0
    except: return False

def pick_cols(df):
    norm = {re.sub(r"\s+","",c).lower(): c for c in df.columns}
    c3 = norm.get("to3am") or norm.get("to03am") or norm.get("3am") or None
    c5 = norm.get("to5am") or norm.get("to05am") or norm.get("5am") or None
    return c3, c5

def load_year(path, year):
    df = pd.read_csv(path)
    lga_col = next((c for c in df.columns if c.lower() in ("lga","lga_name") or "lga (2021)" in c.lower()), None)
    if lga_col:
        df = df[df[lga_col].astype(str).str.strip().str.lower() == CBD_LGA_NAME.lower()].copy()
    df["year"] = year
    c3, c5 = pick_cols(df)
    if c3 is None and c5 is None:
        th_col = next((c for c in df.columns if "trading" in c.lower() or "hours" in c.lower()), None)
        if th_col:
            pat3 = re.compile(r"\bto\s*3\s*am\b", re.IGNORECASE)
            pat5 = re.compile(r"\bto\s*5\s*am\b", re.IGNORECASE)
            v3 = df[th_col].astype(str).str.contains(pat3, na=False)
            v5 = df[th_col].astype(str).str.contains(pat5, na=False)
        else:
            v3 = pd.Series(False, index=df.index)
            v5 = pd.Series(False, index=df.index)
    else:
        v3 = df[c3].map(to_bool) if c3 else pd.Series(False, index=df.index)
        v5 = df[c5].map(to_bool) if c5 else pd.Series(False, index=df.index)
    # tiers: 5am overrides 3am
    tier5 = v5
    tier3 = v3 & (~v5)
    df["to5"] = tier5
    df["to3"] = tier3
    return df

v2022 = load_year(VENUE_2022, 2022)
v2023 = load_year(VENUE_2023, 2023)
v2024 = load_year(VENUE_2024, 2024)
v = pd.concat([v2022, v2023, v2024], ignore_index=True)

out = v.groupby("year", as_index=False).agg(
    total_venues=("to3","size"),
    to3_venues=("to3","sum"),
    to5_venues=("to5","sum"),
)
out["to3_share"] = out["to3_venues"] / out["total_venues"]
out["to5_share"] = out["to5_venues"] / out["total_venues"]
out["area_km2"]  = CBD_AREA_KM2
out["density_km2"]        = out["total_venues"] / CBD_AREA_KM2
out["late_density_3am"]   = out["to3_venues"]   / CBD_AREA_KM2
out["late_density_5am"]   = out["to5_venues"]   / CBD_AREA_KM2

out_path = Path(OUTDIR) / "venues_yearly_metrics.csv"
Path(OUTDIR).mkdir(parents=True, exist_ok=True)
out.to_csv(out_path, index=False)

if Path(ASSAULTS_YR).exists():
    a_tot = pd.read_csv(ASSAULTS_YR)  # year,total_night_window
    # 00–06 sub-window from the night-window file
    if Path(ASSAULTS_NW).exists():
        nw = pd.read_csv(ASSAULTS_NW)
        overnight = nw[(nw["period"]=="12am - < 6am") & (nw["day"].isin(["Saturday","Sunday","Monday"]))]
        a_006 = overnight.groupby("year", as_index=False)["count"].sum().rename(columns={"count":"assaults_00_06"})
    else:
        a_006 = pd.DataFrame(columns=["year","assaults_00_06"])
    m = a_tot.merge(a_006, on="year", how="left").merge(out, on="year", how="inner")
    m["assaults_per_venue"]      = m["total_night_window"] / m["total_venues"]
    m["assaults_per_3am_venue"]  = np.where(m["to3_venues"]>0, m["total_night_window"]/m["to3_venues"], np.nan)
    m["assaults_per_5am_venue"]  = np.where(m["to5_venues"]>0, m["total_night_window"]/m["to5_venues"], np.nan)
    m["assaults_00_06_per_5am"]  = np.where(m["to5_venues"]>0, m["assaults_00_06"]/m["to5_venues"], np.nan)
    m.to_csv(Path(OUTDIR) / "merged_panel_yearly_tiers.csv", index=False)
