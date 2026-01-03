#The code is generated using ChatGPT on November 19, 2025
#Prompts direct the model to:

#1. Write a Python script to calculate the minimum distance between agricultural land locations and nearby rivers or lakes using latitude and longitude data stored in Excel files.

#2. The agricultural land Excel file contains columns: LandName, Latitude, Longitude.
#3. The river/lake Excel file contains columns: RiverName, Latitude, Longitude.

#4. Use the Haversine formula to compute great-circle distances in kilometers.

#5. For each agricultural land point, calculate the minimum distance to any river or lake point and store the result in a new column.

#6. Save the updated agricultural data to a new Excel file.
#
#Note: The code modified as per requirement of the study.

import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# ---------- STEP 1: Define the Haversine distance function ----------
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    R = 6371  # Radius of Earth in kilometers

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance  # in kilometers


# ---------- STEP 2: Load the Excel files ----------
# Replace the file paths below with your actual file names
agri_file = "WakiVillageData.xlsx"
river_file = "WaterZones.xlsx"

# Example structure:
# agri_file: columns = ['LandName', 'Latitude', 'Longitude']
# river_file: columns = ['RiverName', 'Latitude', 'Longitude']

df_agri = pd.read_excel(agri_file)
df_river = pd.read_excel(river_file)


# ---------- STEP 3: Calculate minimum distances ----------
min_distances = []

for idx, agri_row in df_agri.iterrows():
    lat1, lon1 = agri_row['Latitude'], agri_row['Longitude']

    # Calculate all distances from this land to each river/lake point
    distances = df_river.apply(lambda row: haversine(lat1, lon1, row['Latitude'], row['Longitude']), axis=1)

    # Get the minimum distance
    min_distance = distances.min()
    min_distances.append(min_distance)

# Add the calculated distances to the agricultural DataFrame
df_agri['MinDistance_km'] = min_distances


# ---------- STEP 4: Save results to a new Excel file ----------
output_file = "Zone1.xlsx"
df_agri.to_excel(output_file, index=False)

print(f"Minimum distances calculated and saved to '{output_file}'")
