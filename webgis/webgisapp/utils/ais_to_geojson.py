from datetime import timedelta
from django.db.models.query import QuerySet
from .exceptions import *
from geojson import FeatureCollection, Feature, LineString, Point
from .join_travel import Delete_None_Existing_Travels, Comprobe_Outdated_Travels
from random import randrange
from webgisapp.models import AISVessel, Vessel, Travel
from .weight_kg_generator import relateAISKg

colors = [
    "#fe0000",  # Red
    "#fe4600",  # Red Orange
    "#ff7f02",  # Orange
    "#ffb305",  # Orange Yellow
    "#fee002",  # Yellow
    "#7ac043",  # Yellow Green
    "#04a650",  # Green
    "#08a99a",  # Blue Green
    "#1150ff",  # Blue
    "#7208a6",  # Blue Violet
    "#bb00ff",  # Violet
    "#cb01af",  # Red Violet
]


def AISQuery_To_Collection(Vessels, AISQuery, Type, Heat=False, Individual=False):
    """
    From a Vessel and AISVessel (Model) QuerySet creates
    a GeoJSON LineStringCollection

    Parameters:
        (QuerySet, QuerySet)
        returns FeatureCollection
    """

    FormatComprobation(Vessels, AISQuery, Type, Heat)

    features = []
    color = 0
    for Vessel in Vessels:
        AIS_Q = AISQuery.filter(
            MMSI=Vessel
        )  # Buscamos los AIS que concuerden con el vessel
        if len(AIS_Q) > 0:
            if Heat:
                travels = Travel.objects.filter(AIS_fk__in=AIS_Q)
                if Comprobe_Outdated_Travels(travels):
                    Delete_None_Existing_Travels(travels)
                travel_dict = relateAISKg(travels)

            ais_array = []
            ais_group = []
            for ais in AIS_Q:
                # Separamos el AIS por grupos para que no se solapen rutas
                # en las lineas
                if ais == AIS_Q[0]:
                    date_before = ais.BaseDateTime
                date = ais.BaseDateTime
                # Comparamos tiempos del ais y el anterior y
                # lo juntamos por grupos
                if date_before + timedelta(hours=1) < date:
                    ais_array.append(ais_group.copy())
                    ais_group = []
                ais_group.append(ais)
                date_before = ais.BaseDateTime
            ais_array.append(ais_group.copy())

            for ais_g in ais_array:
                if not Individual:
                    f = Feature(
                        # Guardamos posición geográfica
                        geometry=Type([(AIS.LON, AIS.LAT) for AIS in ais_g]),
                        properties={
                            "MMSI": Vessel.MMSI,
                            "VesselName": Vessel.VesselName,
                            "Matricula": Vessel.Matricula,
                            "Color": colors[color % len(colors)],
                            "Image": Vessel.Image,
                        },
                    )
                else:
                    for AIS in ais_g:
                        f = Feature(
                            geometry=Type([(AIS.LON, AIS.LAT)]),
                            properties={
                                "MMSI": Vessel.MMSI,
                                "VesselName": Vessel.VesselName,
                                "Matricula": Vessel.Matricula,
                                "Image": Vessel.Image,
                                "LON": str(AIS.LON)[0:8],
                                "LAT": str(AIS.LAT)[0:8],
                                "COG": AIS.COG,
                                "SOG": AIS.SOG,
                                "BaseDateTime": AIS.BaseDateTime,
                                "CallSign": AIS.CallSign,
                                "VesselType": AIS.VesselType,
                                "Length": AIS.Length,
                                "VWidth": AIS.Width,
                                "Cargo": AIS.Cargo,
                                "TransceiverClass": AIS.TransceiverClass,
                                "Color": colors[color % len(colors)],
                            },
                        )
                        if Heat and len(travels) > 0:
                            # TODO esta mal?
                            # f.properties["Weight"] = travel_dict[travels[0].id]["Kg"]
                            f.properties["Weight"] = randrange(0, 30)
                        elif Heat:
                            f.properties["Weight"] = 0.0
                        features.append(f)
                # if Heat and len(travels) > 0 and travels[0].id in travel_dict:
                if not Individual:
                    if Heat and len(travels) > 0:
                        # TODO esta mal?
                        f.properties["Weight"] = travel_dict[travels[0].id]["Kg"]
                    elif Heat:
                        f.properties["Weight"] = 0.0
                    features.append(f)
                color += 1
    return FeatureCollection(features)


def FormatComprobation(Vessels, AISQuery, Type, Heat):
    if Vessels is None:
        raise EmptyVarException
    elif AISQuery is None:
        raise EmptyVarException
    elif Type is None:
        raise EmptyVarException
    elif Heat is None:
        raise EmptyVarException
    elif not isinstance(Vessels, QuerySet):
        raise InstanceTypeException
    elif not isinstance(AISQuery, QuerySet):
        raise InstanceTypeException
    elif not isinstance(Type, Point.__class__) and not isinstance(
        Type, LineString.__class__
    ):
        raise InstanceTypeException
    elif not isinstance(Heat, bool):
        raise InstanceTypeException
    elif len(Vessels) > 0 and not isinstance(Vessels[0], Vessel):
        raise QueryTypeException
    elif len(AISQuery) and not isinstance(AISQuery[0], AISVessel):
        raise QueryTypeException
