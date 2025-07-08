# ----------------------------------------------
# ORIGINAL PLAN WAS TO USE GEOPY TO GATHER LOCATION DATA, IDEA WAS DISCARDED BECAUSE OF THE AMOUNT OF API CALLS THAT WOULD BE NEEDED
# ----------------------------------------------

import pandas as pd
import geopy as gp
from geopy.geocoders import Nominatim
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="aBaB&&8ololpp",
  database="migration"
)

mycursor = mydb.cursor()
geolocator = Nominatim(user_agent="migration_analysis")

for i in range(1, 2):
    query = (f'SELECT location_long, location_lat FROM migration_data WHERE event_id = {i}')
    mycursor.execute(query)
    long, lat = mycursor.fetchone()
    
    location = geolocator.reverse(f"{lat}, {long}", zoom=10) # Checks up to what city location is in
    sql = (f'UPDATE migration_data SET location = "{location}" WHERE event_id = {i}') 
    mycursor.execute(sql)

mydb.commit()

mycursor.close()
mydb.close()