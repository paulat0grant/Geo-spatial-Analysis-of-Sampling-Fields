#The code is generated using ChatGPT on November 05, 2025
#Prompts direct the model to:
#1. Write a python script to construct Hydrological map
#2. Overlay sampling locations i.e. villages, provided as latitude-longitude points
#3. HydroSHEDS data with HydroLAKES and HydroRIVERS shapfiles were provided in the respecive folder
#4. Associate the color of the sampling villages with soil organic carbon (OC) values
#
#
#Note: The code modified as per requirement of the study.




import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

# ---------------- SETTINGS ----------------
bbox = (73.0, 19.0, 75.0, 22.0)  # (west, south, east, north)
hydro_folder = r"Path to HydroSHEDS files"  
hydro_lakes = os.path.join(hydro_folder, "HydroLAKES_polys_v10.shp")
hydro_rivers = os.path.join(hydro_folder, "HydroRIVERS_v10.shp")
output_png = "Hydrology_with_OC_Villages.png"
# -------------------------------------------

# --- 1. Load HydroLAKES & HydroRIVERS ---
print("Loading HydroLAKES and HydroRIVERS...")
lakes = gpd.read_file(hydro_lakes, bbox=bbox)
rivers = gpd.read_file(hydro_rivers, bbox=bbox)

# Ensure WGS84 (lat/lon) CRS
if lakes.crs != "EPSG:4326":
    lakes = lakes.to_crs("EPSG:4326")
if rivers.crs != "EPSG:4326":
    rivers = rivers.to_crs("EPSG:4326")

print(f"Lakes found: {len(lakes)}")
print(f"Rivers found: {len(rivers)}")

# --- 2. NEW villages with OC% ---
villages_data = [
	{"name":	"V2",	"lat":	19.60553322	,	"lon":	73.73425355	,	"oc":	0.2767	},
	{"name":	"V4",	"lat":	19.57521487	,	"lon":	73.75510083	,	"oc":	0.2785	},
	{"name":	"V1",	"lat":	19.61528372	,	"lon":	73.73647579	,	"oc":	0.1476	},
	{"name":	"V4",	"lat":	19.55200706	,	"lon":	73.74196394	,	"oc":	0.2028	},
	{"name":	"V6",	"lat":	19.56601001	,	"lon":	73.7187476	,	"oc":	0.2421	},
	{"name":	"V3",	"lat":	19.59169673	,	"lon":	73.7458417	,	"oc":	0.2066	},
]

df_villages = pd.DataFrame(villages_data)

# Convert to GeoDataFrame
gdf_villages = gpd.GeoDataFrame(
    df_villages,
    geometry=gpd.points_from_xy(df_villages["Longitude"], df_villages["Latitude"]),
    crs="EPSG:4326"
)

# --- 3. Plot map ---
fig = plt.figure(figsize=(10, 9))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent(bbox)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Plot lakes & rivers
if len(lakes) > 0:
    lakes.plot(ax=ax, color='royalblue', alpha=0.55, transform=ccrs.PlateCarree())
if len(rivers) > 0:
    rivers.plot(ax=ax, color='deepskyblue', linewidth=0.8, transform=ccrs.PlateCarree())

# Plot OC gradient points
sc = ax.scatter(
    gdf_villages["Longitude"], gdf_villages["Latitude"],
    c=gdf_villages["oc"], cmap="plasma",
    s=80, edgecolors="black", transform=ccrs.PlateCarree(),
    label="Av. Zn (mg kg-1)"
)

# Add OC color legend
cbar = plt.colorbar(sc, ax=ax, orientation='vertical', shrink=0.8)
cbar.set_label("Av. Zn (mg kg-1)", fontsize=11)

# Add village names
for _, row in gdf_villages.iterrows():
    ax.text(
        row["Longitude"] + 0.03, row["Latitude"] + 0.03,
        f"{row['name']}",
        fontsize=9, fontweight="bold", transform=ccrs.PlateCarree(), color="black"
    )

plt.title("Hydrological Map with Village \nSoil Zinc level", fontsize=15)
plt.savefig(output_png, dpi=250, bbox_inches="tight")
plt.show()
print(f"✅ Map saved as: {os.path.abspath(output_png)}")
