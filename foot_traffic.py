import pandas as pd
from pathlib import Path

data_dictionary = {
    "Location_Name": "The name of the pedestrian sensor location (street, intersection, or site).",
    "Date": "The full timestamp of the pedestrian count record (YYYY-MM-DD HH:MM:SS).",
    "TotalCount": "The total number of pedestrians recorded by the sensor during that hour.",
    "Hour": "The hour of the day when the count was recorded (0–23, where 0 = midnight, 23 = 11pm).",
    "Day": "The day of the week (Monday–Sunday) extracted from the Date.",
    "DayNo": "The day of the week as a number (0 = Monday, … 6 = Sunday)."
}

file_path = Path("Automatic_Hourly_Pedestrian_Count.csv")

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])

drop_cols = [
    "Location_code", "Week", "LastWeek", "Previous4DayTimeAvg",
    "ObjectId", "LastYear", "Previous52DayTimeAvg"
]
df = df.drop(columns=drop_cols)

df = df[df["Date"].dt.year >= 2023]

friday_night = (
    ((df["Day"] == "Friday") & (df["Hour"] >= 22)) |
    ((df["Day"] == "Saturday") & (df["Hour"] <= 1))
)

saturday_night = (
    ((df["Day"] == "Saturday") & (df["Hour"] >= 22)) |
    ((df["Day"] == "Sunday") & (df["Hour"] <= 1))
)

df = df[friday_night | saturday_night]

df = df.sort_values(by="Date", ascending=False).reset_index(drop=True)

output_file = "Cleaned_Pedestrian_Count.csv"
df.to_csv(output_file, index=False)

print(df.head())

