from geojson import Feature, FeatureCollection, Polygon, MultiPoint
from numpy import arange
import numpy as np
from pprint import pprint
from webgisapp.models import AISVessel, Vessel, Travel
from webgisapp.utils.weight_kg_generator import relateAISKg
from webgisapp.utils.abbr import allTravels


def polygon_mile_geojson(start_point_tuple, end_point_tuple):
    start_lon = start_point_tuple[0]  # Start Longitude
    start_lat = start_point_tuple[1]  # Start Latitude
    end_lon = end_point_tuple[0]  # End Longitude
    end_lat = end_point_tuple[1]  # End Latitude

    # Init point
    LAT = start_lat
    LON = start_lon
    point = start_point_tuple

    # Conditions var for range aprobation
    dict_conditions_lon = {}
    dict_conditions_lat = {}
    dict_points = {}  # Lineal dictionary Points of Polygon
    mult_lat = len(arange(end_lat, start_lat, 0.01))  # Length array Lat
    mult_lon = len(arange(start_lon, end_lon, 0.01))  # Lenght array Lon
    array_lat = arange(end_lat, start_lat, 0.01)
    array_lon = arange(start_lon, end_lon, 0.01)

    f_list = []  # List of features
    i = 0  # Lineal iterator for point dictionary
    for j, y in zip(range(0, mult_lat), array_lat):  # array iterator and value of lat
        for k, x in zip(
            range(0, mult_lon), array_lon
        ):  # array iterator and value of lon
            # 4 points of square
            point = [x, y]
            east_point = [x + 0.01, y]
            south_point = [x, y + 0.01]
            east_south_point = [x + 0.01, y + 0.01]
            if k not in dict_conditions_lon:
                # Save init longitude of square based
                # on matrix col poisition
                dict_conditions_lon[k] = {"x": x}
            if j not in dict_conditions_lat:
                # Save init latitude of square based
                # on matrix row poisition
                dict_conditions_lat[j] = {"y": y}
            dict_points[i] = {
                "polygon": Polygon(
                    [[point, east_point, east_south_point, south_point, point]]
                ),
                "init_point": point,
            }
            i += 1
    # Create weight array matrix
    arr_weight = calculate_weigths_polygons(
        mult_lat, mult_lon, dict_conditions_lon, dict_conditions_lat
    )

    arr_weight_lineal = []
    for col in arr_weight:
        for value in col:
            arr_weight_lineal.append(value)  # Convert matrix to lineal array

    for point_i in range(0, len(dict_points)):
        f = Feature(
            id=point_i,
            geometry=dict_points[point_i]["polygon"],
            properties={
                "weight": arr_weight_lineal[point_i],
                "index": point_i,
                "init_point": dict_points[point_i]["init_point"],
            },
        )
        f_list.append(f)
        k += 1
    return FeatureCollection(f_list)


def in_range(x, lon):
    if x + 0.01 >= lon and x <= lon:
        return True
    else:
        return False


def calculate_weigths_polygons(
    mult_lat, mult_lon, dict_conditions_lon, dict_conditions_lat
):
    arr_weight = np.zeros((mult_lat, mult_lon))  # Init matrix to zeros
    travels = allTravels()
    travel_kg_dict = relateAISKg(travels)
    for travel in travels:
        ais = travel.AIS_fk
        x = -1
        y = -1
        for j in range(0, len(dict_conditions_lat)):
            # Save position in matrix in case in range
            if in_range(dict_conditions_lat[j]["y"], ais.LAT):
                y = j
                break
        for i in range(0, len(dict_conditions_lon)):
            # Save position in matrix in case in range
            if in_range(dict_conditions_lon[i]["x"], ais.LON):
                x = i
                break
        if x != -1 and y != -1:
            # Sum weight of ais to total in position
            arr_weight[y][x] += travel_kg_dict[travel.id]["Kg"]
    pprint(arr_weight)
    return arr_weight


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
