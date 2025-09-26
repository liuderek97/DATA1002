import pandas as pd
import matplotlib.pyplot as plt


df_2024 = pd.read_csv("premises-list-as-at-7-jun-2024.csv")
df_2023 = pd.read_csv("premises-list-as-at-4-dec-2023.csv")
df_2022 = pd.read_csv("premises-list-as-at-8-dec-2022.csv")


trading_status = "Trading"
license_type = ["Liquor - on-premises licence", "Liquor - small bar licence", "Liquor - hotel licence"]
license_status = "Current"
business_type = "Full hotel"


f2024 = df_2024[
    (df_2024['Licence type'].isin(license_type)) &
    (df_2024['Trading Status'] == trading_status) &
    (df_2024['Status'] == license_status) &
    (df_2024['Business type'] == business_type) &
    (df_2024['To 12am'] == "Yes") &
    (df_2024['To 3am'] == "Yes")
].assign(Year=2024)

f2023 = df_2023[
    (df_2023['Licence type'].isin(license_type)) &
    (df_2023['Trading Status'] == trading_status) &
    (df_2023['Status'] == license_status) &
    (df_2023['Business type'] == business_type) &
    (df_2023['To 12am'] == "Yes") &
    (df_2023['To 3am'] == "Yes")
].assign(Year=2023)

f2022 = df_2022[
    (df_2022['Licence type'].isin(license_type)) &
    (df_2022['Trading Status'] == trading_status) &
    (df_2022['Status'] == license_status) &
    (df_2022['Business type'] == business_type) &
    (df_2022['To 12am'] == "Yes") &
    (df_2022['To 3am'] == "Yes")
].assign(Year=2022)


combined = pd.concat([f2022, f2023, f2024], ignore_index=True)


combined.to_csv("premises_late_trading_combined_2022_2024.csv", index=False)

pivot = (combined
         .assign(dummy=1)
         .pivot_table(index="LGA", columns="Year", values="dummy", aggfunc="sum", fill_value=0))


top5 = pivot.sum(axis=1).sort_values(ascending=False).head(5).index
pivot_top5 = pivot.loc[top5].sort_values(
    2024 if 2024 in pivot.columns else pivot.sum(axis=1).name, ascending=False)


ax = pivot_top5.plot(kind="bar", stacked=False, figsize=(8,5))
ax.set_title("Top 5 LGAs by late-trading licensed premises (side-by-side by year)")
ax.set_xlabel("LGA")
ax.set_ylabel("Number of licensed premises")
ax.legend(title="Year")


for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f"{int(height)}",
                    (p.get_x() + p.get_width()/2, height),
                    ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.show()
