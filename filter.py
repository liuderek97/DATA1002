import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("premises-list-as-at-7-jun-2024.csv")

trading_status = "Trading" 
lga =  "Sydney"
postcode = 2000
license_type = ["Liquor - on-premises licence", "Liqour - small bar licence", "Liquor - hotel licence"]
license_status = "Current"
business_type = "Full hotel"
precinct = "Sydney CBD Precinct"
street_names = ["Bridge", "Elizabeth", "Park", "Kent"]
#invalid_business_type = ["Restaurant", "Bottle shops & delivery", "Accomodation", "Catering service,Restaurant", "Catering service", "Vessel",
#                        "Theatre public entertainment venue", "Cooking school", "Co-shared Workspace", "Art gallery", "Delivery Only", "Catering service,Theatre public entertainment venue", "Bar,Catering service,Public arena and events,Public hall,Theatre public entertainment venue"]

df_filter = df[(df['LGA'] == lga) & (df['Licence type'].isin(license_type)) & (df["Trading Status"] == trading_status) 
& (df["Status"] == license_status) & (df['Business type'] == business_type) & (df["To 12am"] == "Yes") & (df["To 3am"] == "Yes") & (df["Suburb"] == "SYDNEY")]

df_filter.to_csv("filtered_premises_list.csv")
