import geopandas as gpd
import numpy as np
import pandas as pd

from pytrack.graph import graph, distance
from pytrack.analytics import visualization 
from pytrack.matching import candidate, mpmatching_utils, mpmatching

import itertools
import networkx as nx
from shapely.geometry import LineString

from preprocess_gpx import getTrace

def create_path(G, trellis, predecessor):
    u, v = list(zip(*[(u, v) for v, u in predecessor.items()][::-1]))
    path = [(u, v) for u, v in zip(u, u[1:])]

    path_elab = [node for u, v in path for node in nx.shortest_path(G, trellis.nodes[u]["candidate"].node_id,
                                                                    trellis.nodes[v]["candidate"].node_id,
                                                                    weight='length')]
    path_elab = [k for k, g in itertools.groupby(path_elab)]
    return path_elab

def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

def createDF(coords):
    df = pd.DataFrame(
            {'latitude': [x[0] for x in coords], 'longitude': [x[1] for x in coords]})
    return gpd.GeoDataFrame(
        df,geometry=gpd.points_from_xy(df.longitude, df.latitude),crs="EPSG:4326")

def mapMatching(filename=None,coords=None):
    if filename:
        trace = getTrace(filename)
        latitude = trace["latitude"].to_list()
        longitude = trace["longitude"].to_list()

        points = [(lat, lon) for lat, lon in zip(latitude, longitude)]
    else:
        trace = createDF(coords)
        points = coords

    north, east = np.max(np.array([*points]), 0)
    south, west = np.min(np.array([*points]), 0)

    # Extract road network graph
    G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south,
                            west, east, 500), simplify=True, network_type='drive')
    G_interp, candidates = candidate.get_candidates(G, points, interp_dist=5, closest=True, radius=30)
    trellis = mpmatching_utils.create_trellis(candidates)
    path_prob, predecessor = mpmatching.viterbi_search(G_interp, trellis, "start", "target")

    path_elab = create_path(G_interp, trellis, predecessor)
    edge = [(lat, lng) for lng, lat in LineString([G_interp.nodes[node]["geometry"] for node in path_elab]).coords]
    
    mapped = [edge[closest_node([trace['latitude'][i],trace['longitude'][i]],edge)] for i in range(len(trace))]
    
    track = {'id': [1], 'geometry': [LineString([G_interp.nodes[node]["geometry"] for node in path_elab])]}
    gdf = gpd.GeoDataFrame(track,crs="EPSG:4326")
    map_df = createDF(mapped)
    return {'track': gdf.to_json(), 'org': trace.to_json(), 'mapped': map_df.to_json()}

