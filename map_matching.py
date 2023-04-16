
from shapely.geometry import LineString
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import json
roads = gpd.read_file('input/sf_streets/sf_streets.shp').to_crs("EPSG:4326")
utm = roads.estimate_utm_crs()
roads = roads.to_crs(utm)
trajectory = gpd.read_file(
    'output/track_points.shp').set_crs("EPSG:4326").to_crs(utm)

utm = roads.estimate_utm_crs()
roads = roads.to_crs(utm)
roads.sindex
buffer = 50
bbox = trajectory.bounds + [-buffer, -buffer, buffer, buffer]

hits = bbox.apply(lambda row: list(roads.sindex.intersection(row)), axis=1)

tmp = pd.DataFrame({
    "ptidx": np.repeat(hits.index, hits.apply(len)),
    "linei": np.concatenate(hits.values)
})

tmp = tmp.join(roads.reset_index(drop=True), on="linei")
tmp = tmp.join(trajectory.geometry.rename("point"), on="ptidx")
tmp = gpd.GeoDataFrame(tmp, geometry="geometry", crs=trajectory.crs)

tmp["snap_dist"] = tmp.geometry.distance(gpd.GeoSeries(tmp.point))


tmp = tmp.loc[tmp.snap_dist <= buffer]
tmp = tmp.sort_values(by=["snap_dist"])

closest = tmp.groupby("ptidx").first()
closest = gpd.GeoDataFrame(closest, geometry="geometry")

pos = closest.geometry.project(gpd.GeoSeries(closest.point))
new_pts = closest.geometry.interpolate(pos)


updated_points = trajectory
updated_points['geometry'] = new_pts
temp = LineString(updated_points['geometry'])
line_df = gpd.GeoDataFrame({'lineid': [1]}, geometry=[temp])

updated_points.set_crs(utm).to_crs(
    "EPSG:4326").to_file("output/projected.shp")
line_df.set_crs(utm).to_crs("EPSG:4326").to_file("output/track.shp")
