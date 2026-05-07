import copernicusmarine
from datetime import datetime,timedelta, timezone
from src.copernicusmarine_Parser import BucketParser
from src.leaflet_maps import mymap, markers_from_geojson, get_ids, filter_markers, seed_from_geopandas
from ipywidgets import HTML
from IPython.display import Image
import geopandas as gpd
import logging
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import xarray as xr
from shapely.geometry import LineString


def geojson_to_gdf_between_dates(url, start_date, end_date):
    """
    Extracts geometries between two dates from a GeoJSON URL and returns a GeoPandas DataFrame.

    Args:
        url (str): URL of the GeoJSON file.
        start_date (str): Start date in "YYYY-MM-DD" format.
        end_date (str): End date in "YYYY-MM-DD" format.

    Returns:
        gpd.GeoDataFrame: DataFrame containing geometries and properties between the dates.
    """
    # Fetch the GeoJSON data
    response = requests.get(url)
    response.raise_for_status()
    geojson_data = response.json()

    # Filter features between the two dates
    matching_features = [
        feature for feature in geojson_data["features"]
        if start_date <= feature["properties"]["date"][:10] <= end_date
    ]

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(matching_features)

    return gdf

import pandas as pd

def gdf_closest_date(gdf, target_date_str="2025-10-20", return_idx=False):
    """
    Returns the closest date to `target_date_str` in the GeoDataFrame and optionally its index.

    Args:
        gdf (GeoDataFrame): Input GeoDataFrame with a 'date' column.
        target_date_str (str): Target date as a string (e.g., "2025-10-20").
        return_idx (bool): If True, also returns the index of the closest date.

    Returns:
        closest_date (Timestamp) or (closest_date, closest_idx) (tuple)
    """
    # Convert the 'date' column to datetime if it's not already
    gdf['date'] = pd.to_datetime(gdf['date'])

    # Define the target date
    target_date = pd.to_datetime(target_date_str)

    # Calculate the absolute time difference in days
    gdf['date_diff'] = (gdf['date'] - target_date).abs()

    # Find the index of the row with the smallest difference
    closest_idx = gdf['date_diff'].idxmin()

    # Get the closest date
    closest_date = gdf.loc[closest_idx, 'date']

    if return_idx:
        return closest_date, closest_idx
    else:
        return closest_date


def write_geojson(ds,filename,crs="EPSG:4326"):
    
    geoms = []
    trajectory_ids = []
    
    for traj_id in range(len(ds.trajectory)):
        # Get lon/lat for this trajectory
        lons = ds.lon.isel(trajectory=traj_id).values
        lats = ds.lat.isel(trajectory=traj_id).values
    
        # Create a LineString for this trajectory
        line = LineString(zip(lons, lats))
        geoms.append(line)
        trajectory_ids.append(traj_id)
    
    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {'trajectory_id': trajectory_ids},
        geometry=geoms,
        crs=crs  # WGS84
    )

    # Save to GeoJSON
    gdf.to_file(filename, driver="GeoJSON")
