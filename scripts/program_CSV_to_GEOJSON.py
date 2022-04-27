import csv, json
from geojson import Feature, FeatureCollection, Point
path = r'/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/project/'
file_name = r'random_route_Alicante.csv'

features = []
with open(path + "csv/" + file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    
    first = True
    for r in reader:
        if first:
            first = False
            continue

        latitude, longitude = map(float, (r[3], r[4]))
        features.append(
            Feature(
                geometry = Point((longitude, latitude)),
                properties = {
                    'MMSI': r[1],
                    'BaseDateTime': r[2],
                    'SOG': r[5],
                    'COG': r[6],
                    'VesselName': r[7],
                    'CallSign': r[8],
                    'VesselType': r[9],
                    'Status': r[10],
                    'Length': r[11],
                    'Width': r[12],
                    'Cargo': r[13],
                    'TransceiverClass': r[14],
                    'Weight': r[15],
                }
            )
        )

collection = FeatureCollection(features)
with open(path + "json/" + file_name + ".json", "w") as f:
    f.write('%s' % collection)
		
