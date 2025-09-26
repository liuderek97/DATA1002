import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("LGA_Alcohol_Related_Time_Day.xlsx",
                   sheet_name="LGA5yrs", skiprows=4, header=[0,1,2])


lga_col     = df.columns[0]
offence_col = df.columns[1]
alcohol_col = df.columns[2]


df[[lga_col, offence_col, alcohol_col]] = df[[lga_col, offence_col, alcohol_col]].ffill()
lga_ser     = df[lga_col].astype(str).str.strip().str.lower()
offence_ser = df[offence_col].astype(str).str.strip().str.lower()
alcohol_ser = df[alcohol_col].astype(str).str.strip().str.lower()

# Targets
target_lgas = ["sydney", "newcastle", "inner west", "canterbury-bankstown", "parramatta"]
year_cols = [
    ('Jul 2022 - Jun 2023', 'Total', '12am - < 6am'),
    ('Jul 2023 - Jun 2024', 'Total', '12am - < 6am'),
    ('Jul 2024 - Jun 2025', 'Total', '12am - < 6am'),
]
year_map = {
    'Jul 2022 - Jun 2023': '2022',
    'Jul 2023 - Jun 2024': '2023',
    'Jul 2024 - Jun 2025': '2024',
}


rows = []
for lga_name in target_lgas:
    mask = (lga_ser == lga_name) & \
           (offence_ser == 'non-domestic violence related assault') & \
           (alcohol_ser == 'alcohol related')
    totals = df.loc[mask, year_cols].apply(pd.to_numeric, errors='coerce').sum(axis=0)
    tmp = totals.reset_index()
    tmp.columns = ['Year_range', 'Scope', 'Time band', 'Count']
    tmp['Year'] = tmp['Year_range'].map(year_map)
    tmp['LGA'] = lga_name.title()
    tmp['Offence type'] = 'Non-domestic violence related assault'
    tmp['Alcohol flag'] = 'Alcohol Related'
    rows.append(tmp[['Year','LGA','Offence type','Alcohol flag','Time band','Count']])

assaults_multi = pd.concat(rows, ignore_index=True)


pivot = assaults_multi.pivot(index='Year', columns='LGA', values='Count').fillna(0)
ax = pivot.plot(kind='bar', figsize=(9,5))
ax.set_title('Alcohol-related non-domestic assaults (12am–6am): selected LGAs')
ax.set_xlabel('Year')
ax.set_ylabel('Total Number of Assaults')
ax.legend(title='LGA')
for p in ax.patches:
    h = p.get_height()
    if pd.notna(h) and h > 0:
        ax.annotate(f'{int(h)}', (p.get_x()+p.get_width()/2, h),
                    ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()


with pd.ExcelWriter('assaults_lgas_12to6am_alcohol_2022to2025.xlsx') as writer:
    assaults_multi.to_excel(writer, index=False, sheet_name='Assaults (tidy)')
    pivot.reset_index().to_excel(writer, index=False, sheet_name='Pivot (Year x LGA)')
