import csv, json
from geojson import Feature, FeatureCollection, Point, LineString

path = r"/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/"
file_name = r"AIS_trace_route.csv"

features = []
MMSI_L = []
MMSI_D = []
with open(path + "csv/" + file_name, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")

    first = True
    for r in reader:
        if first:
            first = False
            continue

        latitude, longitude = map(float, (r[3], r[4]))
        if r[1] not in MMSI_L:
            MMSI_L.append(r[1])
            MMSI_D.append(
                {
                    "MMSI": r[1],
                    "VesselName": r[7],
                    "VesselType": r[9],
                    "Length": r[11],
                    "Width": r[12],
                    "Point": [(longitude, latitude)],
                }
            )
        else:
            i = MMSI_L.index(r[1])
            MMSI_D[i]["Point"].append((longitude, latitude))

for D in MMSI_D:
    features.append(
        Feature(
            geometry=LineString(D["Point"]),
            properties={
                "MMSI": D["MMSI"],
                "VesselName": D["VesselName"],
                "VesselType": D["VesselType"],
                "Length": D["Length"],
                "Width": D["Width"],
            },
        )
    )

collection = FeatureCollection(features)
with open(path + "json/" + file_name + ".json", "w") as f:
    f.write("%s" % collection)
