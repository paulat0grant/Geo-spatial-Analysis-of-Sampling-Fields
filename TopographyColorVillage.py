#The code is generated using ChatGPT on October 18, 2025
#Prompts direct the model to:
#1. Write a python script to construct topographic contour map
#2. Overlay sampling locations i.e. villages, provided as latitude-longitude points
#3. Digital Elevation Model (DEM) data from OpenTopography Global DEM API (SRTMGL3)
# for given geographic bounding box were provided in GeoTIFF files.
#4. Associate the color of the sampling villages with soil organic carbon (OC) values
#
#
#Note: The code modified as per requirement of the study.




import os
import requests
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from rasterio.merge import merge

# ------------------ USER SETTINGS ------------------
API_KEY = "API_KEY_HERE"   
bbox = (72.0, 75.0, 19.0, 22.0)  # (min_lon, max_lon, min_lat, max_lat)
tile_size = 1.0
OC_output_png = "ContourMap_with_OC.png"
DEM_TYPE = "SRTMGL3"
# ---------------------------------------------------

# --- Village and OC data ---
villages = [
	{"name":	"V2",	"lat":	19.60553322	,	"lon":	73.73425355	,	"oc":	0.2767	},
	{"name":	"V4",	"lat":	19.57521487	,	"lon":	73.75510083	,	"oc":	0.2785	},
	{"name":	"V1",	"lat":	19.61528372	,	"lon":	73.73647579	,	"oc":	0.1476	},
	{"name":	"V4",	"lat":	19.55200706	,	"lon":	73.74196394	,	"oc":	0.2028	},
	{"name":	"V6",	"lat":	19.56601001	,	"lon":	73.7187476	,	"oc":	0.2421	},
	{"name":	"V3",	"lat":	19.59169673	,	"lon":	73.7458417	,	"oc":	0.2066	},
]

# Extract arrays for plotting
lats  = np.array([v["lat"] for v in villages])
lons  = np.array([v["lon"] for v in villages])
ocs   = np.array([v["oc"]  for v in villages])
names = [v["name"] for v in villages]

# --- 1. Download DEM tiles ---
min_lon, max_lon, min_lat, max_lat = bbox
lon_tiles = np.arange(min_lon, max_lon, tile_size)
lat_tiles = np.arange(min_lat, max_lat, tile_size)
dem_files = []

for lon0 in lon_tiles:
    for lat0 in lat_tiles:
        lon1 = min(lon0 + tile_size, max_lon)
        lat1 = min(lat0 + tile_size, max_lat)
        dem_file = f"dem_{lon0}_{lat0}.tif"
        dem_files.append(dem_file)

        if not os.path.exists(dem_file):
            print(f"⛰️  Downloading tile: {dem_file}")
            url = (
                f"https://portal.opentopography.org/API/globaldem?"
                f"demtype={DEM_TYPE}&south={lat0}&north={lat1}&west={lon0}&east={lon1}"
                f"&outputFormat=GTiff&API_Key={API_KEY}"
            )
            r = requests.get(url, timeout=300)
            if r.status_code == 200 and "error" not in r.text.lower():
                with open(dem_file, "wb") as f:
                    f.write(r.content)
                print(f"✅ Tile downloaded: {dem_file}")
            else:
                print(f"❌ Tile failed: {dem_file}")
                print("   Status:", r.status_code)
                print("   Response:", r.text)

# --- 2. Merge DEM tiles ---
src_files_to_mosaic = [rasterio.open(f) for f in dem_files if os.path.exists(f)]
if not src_files_to_mosaic:
    raise RuntimeError("No valid DEM tiles downloaded. Check your API key or bounds.")

mosaic, out_trans = merge(src_files_to_mosaic)
for src in src_files_to_mosaic:
    src.close()

print("✅ Merged DEM shape:", mosaic.shape)
print("Elevation range (raw):", np.nanmin(mosaic), np.nanmax(mosaic))

# --- 3. Clean & downsample ---
step = max(1, mosaic.shape[1] // 1500)
elevation = mosaic[0][::step, ::step]
elevation = np.flipud(elevation)
elevation = np.where((elevation < -100) | (elevation > 9000), np.nan, elevation)

lon = np.linspace(min_lon, max_lon, elevation.shape[1])
lat = np.linspace(min_lat, max_lat, elevation.shape[0])
lon_grid, lat_grid = np.meshgrid(lon, lat)

print("Elevation range (clean):", np.nanmin(elevation), np.nanmax(elevation))

# --- 4. Plot with OC data points ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent(bbox)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Background terrain
contours = ax.contourf(
    lon_grid, lat_grid, elevation,
    levels=30, cmap='terrain', transform=ccrs.PlateCarree()
)
plt.colorbar(contours, ax=ax, label='Elevation (m)')

# Overlay OC data points
sc = ax.scatter(
    lons, lats, c=ocs, s=100, cmap='plasma', edgecolors='black',
    transform=ccrs.PlateCarree(), label='Av. Zn (mg kg-1)'
)
cb = plt.colorbar(sc, ax=ax, orientation='vertical', shrink=0.8)
cb.set_label('Av. Zn (mg kg-1)')

# Add village labels
for i, name in enumerate(names):
    ax.text(
        lons[i] + 0.05, lats[i] + 0.05, name,
        transform=ccrs.PlateCarree(),
        fontsize=9, fontweight='bold', color='black'
    )

plt.title("Topographic Contour Map with Village \nSoil Zinc Content", fontsize=16)
plt.savefig(OC_output_png, dpi=200, bbox_inches='tight')
plt.show()
print(f"✅ Map saved as: {os.path.abspath(output_png)}")
