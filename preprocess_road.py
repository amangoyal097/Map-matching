import geopandas as gpd
import json

roads = gpd.read_file('input/sf_streets/sf_streets.shp')

graph = {}

for index, road in roads.iterrows():
    road_geom = road.geometry

    neighbors = roads[roads.intersects(road_geom)]

    graph[road['ID']] = {
        "neighbors":  neighbors['ID'].values[neighbors['ID'].values != road['ID']].tolist()
    }
with open("graph.json", "w") as outfile:
    json.dump(graph, outfile)
