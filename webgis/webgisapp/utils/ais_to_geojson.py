from webgisapp.models import AISVessel, Vessel
from geojson import FeatureCollection, Feature, LineString

colors = [
    "#fe0000", # Red
    "#fe4600", # Red Orange
    "#ff7f02", # Orange
    "#ffb305", # Orange Yellow
    "#fee002", # Yellow
    "#7ac043", # Yellow Green
    "#04a650", # Green
    "#08a99a", # Blue Green
    "#1150ff", # Blue 
    "#7208a6", # Blue Violet
    "#bb00ff", # Violet
    "#cb01af", # Red Violet
]

def AISQuery_To_LineStringCollection(Vessels, AISQuery):
    """ 
    From a Vessel and AISVessel (Model) QuerySet creates
    a GeoJSON LineStringCollection

    Parameters:
        (QuerySet, QuerySet)
        returns FeatureCollection
    """
    features = []
    color = 0
    for Vessel in Vessels:
        AIS_Q = AISQuery.filter(MMSI=Vessel) # Buscamos los AIS que concuerden con el vessel
        if len(AIS_Q) > 0:
            features.append(
                Feature(
                    # Guardamos posición geográfica
                    geometry = LineString([(AIS.LON, AIS.LAT) for AIS in AIS_Q]),
                    properties = {
                        'MMSI': Vessel.MMSI,
                        'VesselName' : Vessel.VesselName,
                        'Matricula' : Vessel.Matricula,
                        'Color' : colors[color % len(colors)]
                    }
                )
            )
            color += 1
    return FeatureCollection(features)

