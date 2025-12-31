# Python Code for Topographic Mapping Soil Sampling Dataset
# along with data of Hydrological Bodies.
# Initial codes were obtained form ChatGPT on 17 - 10 - 2025
# Then modified as per requirement of the study.

import os
import geopandas as gpd
import pandas as pd
import requests
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from rasterio.merge import merge
from shapely.geometry import LineString
from shapely.geometry import Polygon


# ------------------ USER SETTINGS ------------------
API_KEY = "API_KEY_HERE"   
bbox = (72.0, 75.0, 19.0, 22.0)  # (min_lon, max_lon, min_lat, max_lat)
tile_size = 1.0
OC_output_png = "ContourMap_with_OC.png"
DEM_TYPE = "SRTMGL3"
# ---------------------------------------------------



# --- Village and OC data ---
villages = [
	{"name":	"V2"	,	"lat":	19.60553322	,	"lon":	73.73425355	,	"oc":	0.4895	},
	{"name":	"V4"	,	"lat":	19.57521487	,	"lon":	73.75510083	,	"oc":	0.4686	},
	{"name":	"V1"	,	"lat":	19.61528372	,	"lon":	73.73647579	,	"oc":	0.5068	},
	{"name":	"V5"	,	"lat":	19.55200706	,	"lon":	73.74196394	,	"oc":	0.4267	},
	{"name":	"V6"	,	"lat":	19.56601001	,	"lon":	73.7187476	,	"oc":	0.4182	},
	{"name":	"V3"	,	"lat":	19.59169673	,	"lon":	73.7458417	,	"oc":	0.4526	},
]

df_villages = pd.DataFrame(villages)

# Extract arrays for plotting
lats  = np.array([v["lat"] for v in villages])
lons  = np.array([v["lon"] for v in villages])
ocs   = np.array([v["oc"]  for v in villages])
names = [v["name"] for v in villages]

#========================================
# --- Major Dam Data ---
Damss = [
	{"name":	"Wilson Dam"	,	"lat":	19.54746	,	"lon":	73.758238		},
	{"name":	"Waki Dam"	,	"lat":	19.56686	,	"lon":	73.76610		},
	{"name":	"Ghatghar Dam"	,	"lat":	19.542577	,	"lon":	73.665818		},
]

df_Damss = pd.DataFrame(Damss)

# Extract arrays for plotting
latsd  = np.array([v["lat"] for v in Damss])
lonsd  = np.array([v["lon"] for v in Damss])
namesd = [v["name"] for v in Damss]


#========================================
# --- Major Dam Data ---
Lakass = [
	{"name":	"Arthur Hill Lake"	,	"lat":	19.536015	,	"lon":	73.746519		},
	{"name":	"Waki Lake"	,	"lat":	19.57415	,	"lon":	73.767823		},
	{"name":	"Ghatghar\n lake"	,	"lat":	19.545027	,	"lon":	73.658836		},
]

df_Lakass = pd.DataFrame(Lakass)

# Extract arrays for plotting
latsl  = np.array([v["lat"] for v in Lakass])
lonsl  = np.array([v["lon"] for v in Lakass])
namesl = [v["name"] for v in Lakass]


#======================================

# --- Major Dam Data ---
riverss = [
	{"name":	"Waki River"	,	"lat":	19.581837	,	"lon":	73.769212		},
	{"name":	"Pravara River"	,	"lat":	19.544573	,	"lon":	73.776347		},
]

df_riverss = pd.DataFrame(riverss)

# Extract arrays for plotting
latsr  = np.array([v["lat"] for v in riverss])
lonsr  = np.array([v["lon"] for v in riverss])
namesr = [v["name"] for v in riverss]


#======================================

# Lake 1

waterzones_file1 = r"Lake1.xlsx"   # Path to uploaded file



print("Loading Lake1.xlsx ...")
df_wz1 = pd.read_excel(waterzones_file1)

# Expecting columns: Latitude, Longitude
gdf_wz1 = gpd.GeoDataFrame(
    df_wz1,
    geometry=gpd.points_from_xy(df_wz1["Longitude"], df_wz1["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords1 = list(zip(df_wz1["Longitude"], df_wz1["Latitude"]))

# Close the loop by adding the first point at the end
coords1.append(coords1[0])

lake_boundary1 = LineString(coords1)

# Create polygon from the same closed coordinate loop
lake_polygon1 = Polygon(coords1)

#Lake 2

waterzones_file2 = r"Lake2.xlsx"   # Path to uploaded file



print("Loading Lake2.xlsx ...")
df_wz2 = pd.read_excel(waterzones_file2)

# Expecting columns: Latitude, Longitude
gdf_wz2 = gpd.GeoDataFrame(
    df_wz2,
    geometry=gpd.points_from_xy(df_wz2["Longitude"], df_wz2["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords2 = list(zip(df_wz2["Longitude"], df_wz2["Latitude"]))

# Close the loop by adding the first point at the end
coords2.append(coords2[0])

lake_boundary2 = LineString(coords2)

# Create polygon from the same closed coordinate loop
lake_polygon2 = Polygon(coords2)

#Lake 3

waterzones_file3 = r"Lake3.xlsx"   # Path to uploaded file



print("Loading Lake3.xlsx ...")
df_wz3 = pd.read_excel(waterzones_file3)

# Expecting columns: Latitude, Longitude
gdf_wz3 = gpd.GeoDataFrame(
    df_wz3,
    geometry=gpd.points_from_xy(df_wz3["Longitude"], df_wz3["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords3 = list(zip(df_wz3["Longitude"], df_wz3["Latitude"]))

# Close the loop by adding the first point at the end
coords3.append(coords3[0])

lake_boundary3 = LineString(coords3)

# Create polygon from the same closed coordinate loop
lake_polygon3 = Polygon(coords3)

#Lake 4

waterzones_file4 = r"Lake4.xlsx"   # Path to uploaded file



print("Loading Lake4.xlsx ...")
df_wz4 = pd.read_excel(waterzones_file4)

# Expecting columns: Latitude, Longitude
gdf_wz4 = gpd.GeoDataFrame(
    df_wz4,
    geometry=gpd.points_from_xy(df_wz4["Longitude"], df_wz4["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords4 = list(zip(df_wz4["Longitude"], df_wz4["Latitude"]))

# Close the loop by adding the first point at the end
coords4.append(coords4[0])

lake_boundary4 = LineString(coords4)

# Create polygon from the same closed coordinate loop
lake_polygon4 = Polygon(coords4)

#Lake 5

waterzones_file5 = r"Lake5.xlsx"   # Path to uploaded file



print("Loading Lake4.xlsx ...")
df_wz5 = pd.read_excel(waterzones_file5)

# Expecting columns: Latitude, Longitude
gdf_wz5 = gpd.GeoDataFrame(
    df_wz5,
    geometry=gpd.points_from_xy(df_wz5["Longitude"], df_wz5["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords5 = list(zip(df_wz5["Longitude"], df_wz5["Latitude"]))

# Close the loop by adding the first point at the end
coords5.append(coords5[0])

lake_boundary5 = LineString(coords5)

# Create polygon from the same closed coordinate loop
lake_polygon5 = Polygon(coords5)

#Lake 6

waterzones_file6 = r"Lake6.xlsx"   # Path to uploaded file



print("Loading Lake6.xlsx ...")
df_wz6 = pd.read_excel(waterzones_file6)

# Expecting columns: Latitude, Longitude
gdf_wz6 = gpd.GeoDataFrame(
    df_wz6,
    geometry=gpd.points_from_xy(df_wz6["Longitude"], df_wz6["Latitude"]),
    crs="EPSG:4326"
)


# Create a LineString in the order points appear
coords6 = list(zip(df_wz6["Longitude"], df_wz6["Latitude"]))

# Close the loop by adding the first point at the end
coords6.append(coords6[0])

lake_boundary6 = LineString(coords6)

# Create polygon from the same closed coordinate loop
lake_polygon6 = Polygon(coords6)
#=============================

#Add river:Waki1
WakiFile1 = r"Waki1.xlsx"   # Path to uploaded file

print("Loading Waki1.xlsx ...")
df_wf1 = pd.read_excel(WakiFile1)

#Add river:Waki2
WakiFile2 = r"Waki2.xlsx"   # Path to uploaded file

print("Loading Waki2.xlsx ...")
df_wf2 = pd.read_excel(WakiFile2)

#Add river:Waki2
WakiFile3 = r"Waki3.xlsx"   # Path to uploaded file

print("Loading Waki3.xlsx ...")
df_wf3 = pd.read_excel(WakiFile3)

#Add river:Perivere
WakiFile4 = r"Perivere.xlsx"   # Path to uploaded file

print("Loading Perivere.xlsx ...")
df_wf4 = pd.read_excel(WakiFile4)

#=============================

#Add Hydro:Hydro1
WakiHydro1 = r"Hydro1.xlsx"   # Path to uploaded file

print("Loading Hydro1.xlsx ...")
df_wh1 = pd.read_excel(WakiHydro1)

#Add Hydro:Hydro2
WakiHydro2 = r"Hydro2.xlsx"   # Path to uploaded file

print("Loading Hydro2.xlsx ...")
df_wh2 = pd.read_excel(WakiHydro2)

#Add Hydro:Hydro3
WakiHydro3 = r"Hydro3.xlsx"   # Path to uploaded file

print("Loading Hydro3.xlsx ...")
df_wh3 = pd.read_excel(WakiHydro3)

#=============================

#Add ArHydro:ArHydro1
ArHydro1 = r"ArHydro1.xlsx"   # Path to uploaded file

print("Loading ArHydro1.xlsx ...")
df_arh1 = pd.read_excel(ArHydro1)

#Add ArHydro:ArHydro1
ArHydro2 = r"ArHydro2.xlsx"   # Path to uploaded file

print("Loading ArHydro2.xlsx ...")
df_arh2 = pd.read_excel(ArHydro2)

#Add ArHydro:ArHydro1
ArHydro3 = r"ArHydro3.xlsx"   # Path to uploaded file

print("Loading ArHydro3.xlsx ...")
df_arh3 = pd.read_excel(ArHydro3)


#Add ArHydro:ArHydro1
ArHydro4 = r"ArHydro4.xlsx"   # Path to uploaded file

print("Loading ArHydro4.xlsx ...")
df_arh4 = pd.read_excel(ArHydro4)

#Add ArHydro:ArHydro1
ArHydro5 = r"ArHydro5.xlsx"   # Path to uploaded file

print("Loading ArHydro5.xlsx ...")
df_arh5 = pd.read_excel(ArHydro5)

#Add ArHydro:ArHydro1
ArHydro6 = r"ArHydro6.xlsx"   # Path to uploaded file

print("Loading ArHydro6.xlsx ...")
df_arh6 = pd.read_excel(ArHydro6)

#Add ArHydro:ArHydro1
ArHydro7 = r"ArHydro7.xlsx"   # Path to uploaded file

print("Loading ArHydro7.xlsx ...")
df_arh7 = pd.read_excel(ArHydro7)

#Add ArHydro:ArHydro1
ArHydro8 = r"ArHydro8.xlsx"   # Path to uploaded file

print("Loading ArHydro8.xlsx ...")
df_arh8 = pd.read_excel(ArHydro8)
#=================================

#Add Stream:Steam1
Stream1 = r"Stream1.xlsx"   # Path to uploaded file

print("Loading Stream1.xlsx ...")
df_st1 = pd.read_excel(Stream1)

#Add Stream:Steam1
Stream2 = r"Stream2.xlsx"   # Path to uploaded file

print("Loading Stream2.xlsx ...")
df_st2 = pd.read_excel(Stream2)

#Add Stream:Steam1
Stream3 = r"Stream3.xlsx"   # Path to uploaded file

print("Loading Stream3.xlsx ...")
df_st3 = pd.read_excel(Stream3)

#Add Stream:Steam1
Stream4 = r"Stream4.xlsx"   # Path to uploaded file

print("Loading Stream4.xlsx ...")
df_st4 = pd.read_excel(Stream4)

#Add Stream:Steam1
Stream5 = r"Stream5.xlsx"   # Path to uploaded file

print("Loading Stream5.xlsx ...")
df_st5 = pd.read_excel(Stream5)

#Add Stream:Steam1
Stream6 = r"Stream6.xlsx"   # Path to uploaded file

print("Loading Stream6.xlsx ...")
df_st6 = pd.read_excel(Stream6)

#Add Stream:Steam1
Stream7 = r"Stream7.xlsx"   # Path to uploaded file

print("Loading Stream7.xlsx ...")
df_st7 = pd.read_excel(Stream7)

#Add Stream:Steam1
Stream8 = r"Stream8.xlsx"   # Path to uploaded file

print("Loading Stream8.xlsx ...")
df_st8 = pd.read_excel(Stream8)

#Add Stream:Steam1
Stream9 = r"Stream9.xlsx"   # Path to uploaded file

print("Loading Stream9.xlsx ...")
df_st9 = pd.read_excel(Stream9)

#Add Stream:Steam1
Stream10 = r"Stream10.xlsx"   # Path to uploaded file

print("Loading Stream10.xlsx ...")
df_st10 = pd.read_excel(Stream10)

#Add Stream:Steam1
Stream11 = r"Stream11.xlsx"   # Path to uploaded file

print("Loading Stream11.xlsx ...")
df_st11 = pd.read_excel(Stream11)

#Add Stream:Steam1
Stream12 = r"Stream12.xlsx"   # Path to uploaded file

print("Loading Stream12.xlsx ...")
df_st12 = pd.read_excel(Stream12)

#Add Stream:Steam1
Stream14 = r"Stream14.xlsx"   # Path to uploaded file

print("Loading Stream14.xlsx ...")
df_st14 = pd.read_excel(Stream14)

#Add Stream:Steam1
Stream15 = r"Stream15.xlsx"   # Path to uploaded file

print("Loading Stream15.xlsx ...")
df_st15 = pd.read_excel(Stream15)

#Add Stream:Steam1
Stream16 = r"Stream16.xlsx"   # Path to uploaded file

print("Loading Stream16.xlsx ...")
df_st16 = pd.read_excel(Stream16)

#Add Stream:Steam1
Stream17 = r"Stream17.xlsx"   # Path to uploaded file

print("Loading Stream17.xlsx ...")
df_st17 = pd.read_excel(Stream17)

#=================================
Dam_file1 = r"Dams.xlsx"   # Path to uploaded file

print("Loading Dams.xlsx ...")
df_df1 = pd.read_excel(Dam_file1)

# Expecting columns: Latitude, Longitude
gdf_df1 = gpd.GeoDataFrame(
    df_df1,
    geometry=gpd.points_from_xy(df_df1["Longitude"], df_df1["Latitude"]),
    crs="EPSG:4326"
)

Dam_file2 = r"Dams2.xlsx"   # Path to uploaded file

print("Loading Dams.xlsx ...")
df_df2 = pd.read_excel(Dam_file2)

# Expecting columns: Latitude, Longitude
gdf_df2 = gpd.GeoDataFrame(
    df_df2,
    geometry=gpd.points_from_xy(df_df2["Longitude"], df_df2["Latitude"]),
    crs="EPSG:4326"
)


#=================================

Wellsfile1 = r"WellsArthur.xlsx"   # Path to uploaded file

print("Loading Wells.xlsx ...")
df_ww1 = pd.read_excel(Wellsfile1)

# Expecting columns: Latitude, Longitude
gdf_ww1 = gpd.GeoDataFrame(
    df_ww1,
    geometry=gpd.points_from_xy(df_ww1["Longitude"], df_ww1["Latitude"]),
    crs="EPSG:4326"
)



#=================================
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
            print(f"Downloading tile: {dem_file}")
            url = (
                f"https://portal.opentopography.org/API/globaldem?"
                f"demtype={DEM_TYPE}&south={lat0}&north={lat1}&west={lon0}&east={lon1}"
                f"&outputFormat=GTiff&API_Key={API_KEY}"
            )
            r = requests.get(url, timeout=300)
            if r.status_code == 200 and "error" not in r.text.lower():
                with open(dem_file, "wb") as f:
                    f.write(r.content)
                print(f"Tile downloaded: {dem_file}")
            else:
                print(f" Tile failed: {dem_file}")
                print("   Status:", r.status_code)
                print("   Response:", r.text)

# --- 2. Merge DEM tiles ---
src_files_to_mosaic = [rasterio.open(f) for f in dem_files if os.path.exists(f)]
if not src_files_to_mosaic:
    raise RuntimeError("No valid DEM tiles downloaded. Check your API key or bounds.")

mosaic, out_trans = merge(src_files_to_mosaic)
for src in src_files_to_mosaic:
    src.close()

print("Merged DEM shape:", mosaic.shape)
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
plt.colorbar(contours, ax=ax, label='Elevation (m)', shrink=0.8, pad=0.1)

# Overlay OC data points
sc = ax.scatter(
    lons, lats, c="green", s=200, edgecolors='green',
    transform=ccrs.PlateCarree(), label='OC (%)'
)

# Add village labels
for i, name in enumerate(names):
    ax.text(
        lons[i] - 0.0020, lats[i] - 0.0020, name,
        transform=ccrs.PlateCarree(),
        fontsize=9, fontweight=1000, color='#F88379'
    )


# Overlay OC data points
sc = ax.scatter(
    lonsd, latsd, c="red", s=50, edgecolors='black', marker="s",
    transform=ccrs.PlateCarree(), label=''
)

    
# Add Dam labels
for i, name in enumerate(namesd):
    ax.text(
        lonsd[i] + 0.0015, latsd[i] + 0.0015, name,
        transform=ccrs.PlateCarree(),
        fontsize=7, fontweight='bold', color='black'
    )
#=========================    
#Lake1
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon1],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary1],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)

#Lake2
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon2],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary2],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)

#Lake2
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon3],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary3],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)

#Lake2
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon4],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary4],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)

#Lake2
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon5],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary5],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)

#Lake2
    
# Plot Water Zones points (black)

# Fill the lake region
ax.add_geometries(
    [lake_polygon6],
    crs=ccrs.PlateCarree(),
    facecolor="#191970",   # Fill color
    edgecolor="#191970",   # Border color
    alpha=0.5,             # Slight transparency so terrain is visible
    label="Lake Region"
)

# Plot outline again on top of fill
ax.add_geometries(
    [lake_boundary6],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="#000000",
    linewidth=0.8
)
#========================
# -----------------------------
# 1) Plot individual dots
# -----------------------------

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------

# Plot river line WITHOUT border
ax.plot(
    df_wf1["Longitude"], df_wf1["Latitude"],
    color="#5E3FD3",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    label="Waki1 River"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wf2["Longitude"], df_wf2["Latitude"],
    color="#5E3FD3",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    label="Waki2 River"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wf3["Longitude"], df_wf3["Latitude"],
    color="#5E3FD3",
    linewidth=2,
    transform=ccrs.PlateCarree(),
    label="Waki3 River"
)


# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wf4["Longitude"], df_wf4["Latitude"],
    color="#191970",
    linewidth=2.5,
    transform=ccrs.PlateCarree(),
    label="Perivere River"
)
#=================

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wh1["Longitude"], df_wh1["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver1"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wh2["Longitude"], df_wh2["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_wh3["Longitude"], df_wh3["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

#=================

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh1["Longitude"], df_arh1["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh2["Longitude"], df_arh2["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh3["Longitude"], df_arh3["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh4["Longitude"], df_arh4["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh5["Longitude"], df_arh5["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh6["Longitude"], df_arh6["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh7["Longitude"], df_arh7["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_arh8["Longitude"], df_arh8["Latitude"],
    color="#0096FF",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

#=================

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st1["Longitude"], df_st1["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st2["Longitude"], df_st2["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st3["Longitude"], df_st3["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st4["Longitude"], df_st4["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st5["Longitude"], df_st5["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st6["Longitude"], df_st6["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st7["Longitude"], df_st7["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st8["Longitude"], df_st8["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st9["Longitude"], df_st9["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st10["Longitude"], df_st10["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st11["Longitude"], df_st11["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st12["Longitude"], df_st12["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st14["Longitude"], df_st14["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st15["Longitude"], df_st15["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st16["Longitude"], df_st16["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)


# -----------------------------
# 2) Connect dots in exact given order
# -----------------------------


# Plot river line WITHOUT border
ax.plot(
    df_st17["Longitude"], df_st17["Latitude"],
    color="#00A36C",
    linewidth=1.5,
    transform=ccrs.PlateCarree(),
    label="HydroRiver2"
)

#=================
# Plot Dams points (black)
ax.scatter(
    gdf_df1["Longitude"], gdf_df1["Latitude"],
    color="#FF4433", s=15, marker="x",
    transform=ccrs.PlateCarree(),
    label="Dams Points"
)

# Plot Dams points (black)
ax.scatter(
    gdf_df2["Longitude"], gdf_df2["Latitude"],
    color="#800000", s=30, marker="X",
    transform=ccrs.PlateCarree(),
    label="Dams Points"
)

#=================
# Plot Wells points (black)
ax.scatter(
    gdf_ww1["Longitude"], gdf_ww1["Latitude"],
    color="#000000", s=10, marker="o",
    transform=ccrs.PlateCarree(),
    label="Wells"
)

#=================
# Add Dam labels
for i, name in enumerate(namesl):
    ax.text(
        lonsl[i] - 0.0015, latsl[i] - 0.0015, name,
        transform=ccrs.PlateCarree(),
        fontsize=7, fontweight='bold', color='black'
    )

# Add river labels
for i, name in enumerate(namesr):
    ax.text(
        lonsr[i] + 0.0005, latsr[i] + 0.0005, name,
        transform=ccrs.PlateCarree(),
        fontsize=6, fontweight='bold', color='blue'
    )

#=================
plt.title("Topographic Contour Map with Villages\n and Hydrological Bodies ", fontsize=16)
plt.savefig(OC_output_png, dpi=200, bbox_inches='tight')
plt.show()
print(f"Map saved as: {os.path.abspath(output_png)}")
