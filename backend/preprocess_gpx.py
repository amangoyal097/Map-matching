import gpxpy
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopy.distance import geodesic

def getTrace(filename):
    gpx_path = filename
    with open(gpx_path) as f:
        gpx = gpxpy.parse(f)

    latitude = []
    longitude = []
    time = []
    speeds = []
    for segment in gpx.tracks[0].segments:
        for index, p in enumerate(segment.points):
            try:
                if not p.time or not p.latitude or not p.longitude:
                    continue
                distance = None
                if len(latitude) > 0:
                    distance = geodesic(
                        (p.latitude, p.longitude), (latitude[-1], longitude[-1])).meters
                speed = None if distance == None else distance / \
                    (p.time - time[-1]).total_seconds()
                if speed != None and speed < 0.5:
                    continue
                latitude.append(p.latitude)
                longitude.append(p.longitude)
                time.append(p.time)
                speeds.append(speed)
            except Exception as e:
                print(e)
                pass
    df = pd.DataFrame(
        {'latitude': latitude, 'longitude': longitude, 'time': time, 'speed': speed})
    gdf = gpd.GeoDataFrame(
        df.drop('time', axis=1), geometry=gpd.points_from_xy(df.longitude, df.latitude),crs="EPSG:4326")
    return gdf
