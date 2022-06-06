from geojson import Feature, FeatureCollection, Polygon, MultiPoint
from numpy import arange
import numpy as np
from webgisapp.models import AISVessel, Vessel, Travel
from webgisapp.utils.weight_kg_generator import relateAISKg
from webgisapp.utils.abbr import allTravels


def polygon_mile_geojson(start_point_tuple, end_point_tuple):
    start_lon = start_point_tuple[0]
    start_lat = start_point_tuple[1]
    end_lon = end_point_tuple[0]
    end_lat = end_point_tuple[1]

    LAT = start_lat
    LON = start_lon
    point = start_point_tuple

    dict_conditions_lon = {}
    dict_conditions_lat = {}
    dict_points = {}
    mult_lat = len(arange(end_lat, start_lat, 0.01))
    mult_lon = len(arange(start_lon, end_lon, 0.01))
    array_lat = arange(end_lat, start_lat, 0.01)
    array_lon = arange(start_lon, end_lon, 0.01)

    print(mult_lat)
    print(mult_lon)
    f_list = []
    i = 0
    # for j, y in zip(range(0, mult_lat), array_lat):
    #     for i, x in zip(range(0, mult_lon), array_lon):
    for j, y in zip(range(0, mult_lat), array_lat):
        for k, x in zip(range(0, mult_lon), array_lon):
            point = [x, y]
            east_point = [x + 0.01, y]
            south_point = [x, y + 0.01]
            east_south_point = [x + 0.01, y + 0.01]
            if k not in dict_conditions_lon:
                dict_conditions_lon[k] = {"x": x}
            if j not in dict_conditions_lat:
                dict_conditions_lat[j] = {"y": y}
            dict_points[i] = Polygon(
                [[point, east_point, east_south_point, south_point, point]]
            )
            i += 1
    print(dict_conditions_lat)
    print(dict_conditions_lon)
    arr_weight = calculate_weigths_polygons(
        mult_lat, mult_lon, dict_conditions_lon, dict_conditions_lat
    )
    print(arr_weight)

    arr_weight_lineal = []
    for col in arr_weight:
        for value in col:
            arr_weight_lineal.append(value)

    for point_i in range(0, len(dict_points)):
        f = Feature(
            id=point_i,
            geometry=dict_points[point_i],
            properties={"weight": arr_weight_lineal[point_i]},
        )
        f_list.append(f)
        k += 1
    return FeatureCollection(f_list)

    #     if (z + 1) % mult_lon == 0:
    #         k += 1
    #     z = (z + 1) % mult_lon


def in_range(x, lon):
    if x + 0.01 >= lon and x <= lon:
        return True
    else:
        return False


def calculate_weigths_polygons(
    mult_lat, mult_lon, dict_conditions_lon, dict_conditions_lat
):
    arr_weight = np.zeros((mult_lat, mult_lon))
    travels = allTravels()
    travel_kg_dict = relateAISKg(travels)
    for travel in travels:
        ais = travel.AIS_fk
        x = -1
        y = -1
        for j in range(0, len(dict_conditions_lat)):
            print("id" + str(j))
            if in_range(dict_conditions_lat[j]["y"], ais.LAT):
                y = j
                break
        for i in range(0, len(dict_conditions_lon)):
            if in_range(dict_conditions_lon[i]["x"], ais.LON):
                x = i
                break
        if x != -1 and y != -1:
            arr_weight[y][x] += travel_kg_dict[travel.id]["Kg"]
        x = -1
        y = -1
    return arr_weight


import sys


def search_min_max_ais(aiss=None):
    if aiss is None:
        aiss = AISVessel.objects.all()
    lon_list = aiss.values_list("LON", flat=True)
    lat_list = aiss.values_list("LAT", flat=True)
    min_lon = min(lon_list, key=lambda x: float(x))
    max_lon = max(lon_list, key=lambda x: float(x))
    min_lat = min(lat_list, key=lambda x: float(x))
    max_lat = max(lat_list, key=lambda x: float(x))
    return (min_lon - 0.01, max_lat + 0.01), (max_lon + 0.01, min_lat - 0.01)
