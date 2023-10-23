import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def count_sinkings_within_area(df, min_lat, max_lat, min_lon, max_lon):
    count = 0
    for _, row in df.iterrows():
        lat, lon = eval(row['coordinates'])[0]
        lat, lon = float(lat), float(lon)
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            count += 1
    return count


def find_min_max_lat_lon(df):
    min_lat, max_lat = 90, -90
    min_lon, max_lon = 180, -180

    for _, row in df.iterrows():
        lat, lon = eval(row['coordinates'])[0]
        lat, lon = float(lat), float(lon)
        min_lat = min(min_lat, lat)
        max_lat = max(max_lat, lat)
        min_lon = min(min_lon, lon)
        max_lon = max(max_lon, lon)

    return min_lat, max_lat, min_lon, max_lon


def create_subregions(min_lat, max_lat, min_lon, max_lon, lat_splits, lon_splits):
    lat_step = (max_lat - min_lat) / lat_splits
    lon_step = (max_lon - min_lon) / lon_splits

    subregions = []
    for i in range(lat_splits):
        for j in range(lon_splits):
            subregions.append(
                (
                    min_lat + i * lat_step,
                    min_lat + (i + 1) * lat_step,
                    min_lon + j * lon_step,
                    min_lon + (j + 1) * lon_step,
                )
            )
    return subregions


def get_location_name(lat, lon):
    geolocator = Nominatim(user_agent="myGeocoder")
    try:
        location = geolocator.reverse((lat, lon), timeout=10)
        if location:
            return location.address.split(", ")[-1]
        else:
            return "Unknown"
    except GeocoderTimedOut:
        return "Unknown"


filename = 'data/converted_merchants_data.csv'
df = pd.read_csv(filename)

min_lat, max_lat, min_lon, max_lon = find_min_max_lat_lon(df)

lat_splits = int(np.sqrt(50))
lon_splits = int(np.sqrt(50))
subregions = create_subregions(min_lat, max_lat, min_lon, max_lon, lat_splits, lon_splits)

results = {}
for i, area in enumerate(subregions):
    min_lat, max_lat, min_lon, max_lon = area
    region_total = count_sinkings_within_area(df, min_lat, max_lat, min_lon, max_lon)
    region_name = f"({min_lat:.2f},{min_lon:.2f})-({max_lat:.2f},{max_lon:.2f})"
    results[region_name] = region_total

threshold = 10

filtered_results = {name: count for name, count in results.items() if count > threshold}

names = list(filtered_results.keys())
values = list(filtered_results.values())

plt.figure(figsize=(20, 6))
plt.bar(names, values, color="red")
plt.xlabel("Region")
plt.ylabel("Liczba zatopień")
plt.title("Częstotliwość zatopień w zależności od regionu")
plt.yscale('log')
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.2)

labels = ['Region ' + str(i+1) for i in range(len(names))]
plt.xticks(range(len(names)), labels)

plt.savefig("coordinates.png")
plt.show()

for i, label in enumerate(labels):
    print(f"{label}: {names[i]}")

