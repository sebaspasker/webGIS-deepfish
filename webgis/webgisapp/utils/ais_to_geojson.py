from webgisapp.models import AISVessel, Vessel, Travel
from geojson import FeatureCollection, Feature, LineString, Point
from .weight_kg_generator import relateAISKg

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

def AISQuery_To_Collection(Vessels, AISQuery, Type, Heat=False):
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
            if Heat:
                travels = Travel.objects.filter(AIS_fk__in=AIS_Q)
                travel_dict = relateAISKg(travels)
            f = Feature(
                # Guardamos posición geográfica
                geometry = Type([(AIS.LON, AIS.LAT) for AIS in AIS_Q]),
                properties = {
                    'MMSI': Vessel.MMSI,
                    'VesselName' : Vessel.VesselName,
                    'Matricula' : Vessel.Matricula,
                    'Color' : colors[color % len(colors)],
                })
            if Heat and len(travels) > 0:
                f.properties['Weight'] = travel_dict[travels[0].id]['Kg']
            features.append(f)
            color += 1
    return FeatureCollection(features)

