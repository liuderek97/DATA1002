import pandas as pd
import matplotlib.pyplot as plt
df_2024 = pd.read_csv("premises-list-as-at-7-jun-2024.csv")
df_2023 = pd.read_csv("premises-list-as-at-4-dec-2023.csv")
df_2022 = pd.read_csv("premises-list-as-at-8-dec-2022.csv")

trading_status = "Trading" 
lga =  "Sydney"
postcode = 2000
license_type = ["Liquor - on-premises licence", "Liquor - small bar licence", "Liquor - hotel licence"]
license_status = "Current"
business_type = "Full hotel"
precinct = "Sydney CBD Precinct"
street_names = ["Bridge", "Elizabeth", "Park", "Kent"]
#invalid_business_type = ["Restaurant", "Bottle shops & delivery", "Accomodation", "Catering service,Restaurant", "Catering service", "Vessel",
#                        "Theatre public entertainment venue", "Cooking school", "Co-shared Workspace", "Art gallery", "Delivery Only", "Catering service,Theatre public entertainment venue", "Bar,Catering service,Public arena and events,Public hall,Theatre public entertainment venue"]

df_2024_filter = df_2024[
  (df_2024['LGA'] == lga) 
  & (df_2024['Licence type'].isin(license_type)) 
  & (df_2024["Trading Status"] == trading_status) 
  & (df_2024["Status"] == license_status) 
  & (df_2024['Business type'] == business_type) 
  & (df_2024["To 12am"] == "Yes") 
  & (df_2024["To 3am"] == "Yes") 
  & (df_2024["Suburb"] == "SYDNEY")
  ]

df_2023_filter = df_2023[
  (df_2023['LGA'] == lga)
  & (df_2023['Licence type'].isin(license_type)) 
  & (df_2023["Trading Status"] == trading_status) 
  & (df_2023["Status"] == license_status) 
  & (df_2023['Business type'] == business_type) 
  & (df_2023["To 12am"] == "Yes") 
  & (df_2023["To 3am"] == "Yes") 
  & (df_2023["Suburb"] == "SYDNEY")
  ]

df_2022_filter = df_2022[
  (df_2022['LGA'] == lga)
  & (df_2022['Licence type'].isin(license_type)) 
  & (df_2022["Trading Status"] == trading_status) 
  & (df_2022["Status"] == license_status) 
  & (df_2022['Business type'] == business_type) 
  & (df_2022["To 12am"] == "Yes") 
  & (df_2022["To 3am"] == "Yes") 
  & (df_2022["Suburb"] == "SYDNEY")
                         ]

count_2024 = len(df_2024_filter)
count_2023 = len(df_2023_filter)
count_2022 = len(df_2022_filter)


plt.figure(figsize=(6,4))

years = ["2022" ,"2023", "2024"]
counts = [count_2022, count_2023, count_2024]

plt.bar(years,counts, width=0.5)
plt.xlabel("Year")
plt.ylabel("Number of licensed premises")
plt.title("Licensed premises 2024")

for x, y in zip(years, counts):
    plt.text(x, y, str(y), ha="center", va="bottom")
    
plt.show()

df_2024_filter.to_csv("filtered_premises_list_2024.csv")
df_2023_filter.to_csv("filtered_premises_list_2023.csv")
df_2022_filter.to_csv("filtered_premises_list_2022.csv")
