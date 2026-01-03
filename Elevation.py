#The code is generated using ChatGPT on November 29, 2025
#Prompts direct the model to:
#1. Write a python script to extract the elevation of sampling locations
#2. The sampling locations i.e. villages, provided as latitude-longitude points 
#3. Digital Elevation Model (DEM) data from OpenTopography Global DEM API (SRTMGL3)
# for given geographic bounding box were provided in GeoTIFF files.
#4. Save the extracted data in excel sheet.
#
#Note: The code modified as per requirement of the study.




import os
import requests
import rasterio
import numpy as np
import pandas as pd
from rasterio.merge import merge

# ------------------ USER SETTINGS ------------------
API_KEY = "YOUR_API_KEY_HERE"     # Replace with your OpenTopography API key
bbox = (72.0, 75.0, 19.0, 22.0)    # (min_lon, max_lon, min_lat, max_lat)
tile_size = 1.0
DEM_TYPE = "SRTMGL3"
EXCEL_OUTPUT = "village_elevation.xlsx"
# ---------------------------------------------------

# --- Village info ---
villages = [
    {"name": "V2",           "lat": 19.60553322, "lon": 73.73425355},
    {"name": "V4",     "lat": 19.57521487, "lon": 73.75510083},
    {"name": "V1","lat": 19.61528372, "lon": 73.73647579},
    {"name": "V5",       "lat": 19.55200706, "lon": 73.74196394},
    {"name": "V6",       "lat": 19.56601001, "lon": 73.7187476},
    {"name": "V3",      "lat": 19.59169673, "lon": 73.7458417},
]

# --- 1. Download DEM tiles ---
min_lon, max_lon, min_lat, max_lat = bbox
lon_tiles = np.arange(min_lon, max_lon, tile_size)
lat_tiles = np.arange(min_lat, max_lat, tile_size)
dem_files = []

for lon0 in lon_tiles:
    for lat0 in lat_tiles:
        lon1 = min(lon0 + tile_size, max_lon)
        lat1 = min(lat0 + tile_size, max_lat)

        dem_file = f"dem_{lon0:.2f}_{lat0:.2f}.tif"
        dem_files.append(dem_file)

        if not os.path.exists(dem_file):
            print(f"Downloading DEM tile: {dem_file}")
            url = (
                f"https://portal.opentopography.org/API/globaldem?"
                f"demtype={DEM_TYPE}&south={lat0}&north={lat1}&west={lon0}&east={lon1}"
                f"&outputFormat=GTiff&APIKey={API_KEY}"
            )
            r = requests.get(url, timeout=300)

            if r.status_code == 200 and "error" not in r.text.lower():
                with open(dem_file, "wb") as f:
                    f.write(r.content)
                print(" → Downloaded")
            else:
                print(" → Failed:", r.text)

# --- 2. Merge tiles ---
src_list = [rasterio.open(f) for f in dem_files if os.path.exists(f)]
if not src_list:
    raise RuntimeError("No DEM files available.")

mosaic, transform = merge(src_list)
for src in src_list:
    src.close()

mosaic = mosaic[0]    # DEM band 1

# --- 3. Extract elevation for each village ---
def get_elevation(lat, lon):
    """Return elevation at (lat, lon) from merged DEM."""
    row, col = rasterio.transform.rowcol(transform, lon, lat)
    if 0 <= row < mosaic.shape[0] and 0 <= col < mosaic.shape[1]:
        return float(mosaic[row, col])
    else:
        return np.nan

# Build results
results = []
for v in villages:
    elevation = get_elevation(v["lat"], v["lon"])
    results.append({
        "Village": v["name"],
        "Latitude": v["lat"],
        "Longitude": v["lon"],
        "Elevation_m": elevation
    })

# --- 4. Save to Excel ---
df = pd.DataFrame(results)
df.to_excel(EXCEL_OUTPUT, index=False)

print(f"\n✅ Elevation extracted for all villages.")
print(f"📁 Saved Excel file: {os.path.abspath(EXCEL_OUTPUT)}")





