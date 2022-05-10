from webgisapp.models import AISVessel, Vessel
from geojson import FeatureCollection, Feature, LineString

def AISQuery_To_LineStringCollection(Vessels, AISQuery):
    """ 
    From a Vessel and AISVessel (Model) QuerySet creates
    a GeoJSON LineStringCollection

    Parameters:
        (QuerySet, QuerySet)
        returns FeatureCollection
    """
    features = []
    for Vessel in Vessels:
        AIS_Q = AISQuery.filter(MMSI=Vessel)
        if len(AIS_Q) > 0:
            features.append(
                Feature(
                    geometry = LineString([(AIS.LON, AIS.LAT) for AIS in AIS_Q]),
                    properties = {
                        'MMSI': Vessel.MMSI,
                        'VesselName' : Vessel.VesselName,
                        'Matricula' : Vessel.Matricula
                    }
                )
            )
    return FeatureCollection(features)

