from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import geopy.distance
import math

f = pd.read_csv("raw_data.csv", quotechar='"')

# Group data for each goose in periods of 3 days + Start data from 2017-08-08
f = f[f['timing']>'2017-08-08']
f["timing"] = pd.to_datetime(f["timing"]).dt.floor('D').apply(lambda a : datetime.fromordinal(a.toordinal() - (a.toordinal() % 3))) # figure out how to get the modulo thing working

f = f.sort_values("timing").reset_index()

f["prev_lat"] = f.groupby("individual_local_identifier")["location_lat"].shift(1)
f["prev_long"] = f.groupby("individual_local_identifier")["location_long"].shift(1)

# geopy dist is taking too long so haversine formula for dist
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers
    return c * r

def calc_dist(row):
    if not math.isnan(row["prev_lat"]):
        return haversine(row["location_lat"], row["location_long"], row["prev_lat"], row["prev_long"])
    else:
        return 0

f["step_distance"] = f.apply(calc_dist, axis=1)
f["month"] = f["timing"].dt.to_period("M")
monthly_goose_dist = f.groupby(["month", "individual_local_identifier"])["step_distance"].sum().reset_index(name="total_month_dist")
avg_goose_dist = monthly_goose_dist.groupby("month")["total_month_dist"].mean().reset_index(name="avg_month_dist")

avg_goose_dist = avg_goose_dist.sort_values("month")
avg_goose_dist["month_formatted"] = avg_goose_dist["month"].dt.strftime("%Y-%m")
fig = px.bar(avg_goose_dist, x='month_formatted', y='avg_month_dist', labels={"month_formatted":"Month", "avg_month_dist":"Average Distance (km)"})
fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 10}, title="Monthly Distance Travelled by NE American Canada Geese 2017-2021", )
fig.update_xaxes(ticks='outside', ticklen=10, ticklabelindex=-1, tickangle=45)
fig.write_image("results\\movement_per_month.png") 