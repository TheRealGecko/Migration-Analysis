from datetime import datetime
import pandas as pd
import plotly.express as px

f = pd.read_csv("raw_data.csv", quotechar='"')
f = f[f['timing']>'2017-08-08']
f["timing"] = pd.to_datetime(f["timing"]).dt.floor('D').apply(lambda a : datetime.fromordinal(a.toordinal() - (a.toordinal() % 3))) # figure out how to get the modulo thing working
grouped_times = f.groupby(["timing", "individual_local_identifier"]).mean(["location_long","location_lat"]).reset_index()

fig =  px.density_map(grouped_times, lat="location_lat", lon="location_long", animation_frame="timing", radius=10,
        center=dict(lat=52.0, lon=-78.0), zoom=3,
        map_style="open-street-map")

fig.update_layout(margin={"r": 20, "t": 50, "l": 20, "b": 10}, title="North-East American Canada Goose Migration 2017-2021")

fig.write_html('results\\mapped_data.html')