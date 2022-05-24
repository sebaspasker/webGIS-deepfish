from webgisapp.models import *
from .ais_to_geojson import AISQuery_To_Collection
from .exceptions import *
from geojson import LineString, Point, MultiPoint
import datetime


def Filter_Route(MMSI=None, date_from=None, date_to=None, talla=None, pez=None):
    """
    Comprueba los objetos que no estén vaciós de las variables:
        MMSI, fecha inicio, fecha fin, talla, pez
    Y mete un filtrado en la base de datos en base a esos parámetros.
    """
    null_q = []
    if (isinstance(MMSI, str) and len(MMSI) == 0) or (
        isinstance(pez, str) and len(pez) == 0
    ):
        raise EmptyVarException
    for var in [
        MMSI,
        date_from,
        date_to,
        talla,
        pez,
    ]:  # Comprobamos los parámetros vacíos
        if var is None:
            null_q.append(False)
        elif isinstance(var, str) and "".__eq__(var):
            null_q.append(False)
        else:
            null_q.append(True)

    # En caso que esté todo vacío buscamos en base a todo
    ais = AISVessel.objects.all()
    vessel = Vessel.objects.all()
    plate = Plate.objects.all()
    for notNull, i in zip(null_q, range(5)):  # Filtrado
        if i == 0 and notNull:
            # Busquedad en base al MMSI
            vessel = vessel.filter(MMSI__contains=MMSI)
            ais = ais.filter(MMSI__in=vessel)
        elif i == 2 and notNull:
            # Busquedad en base a rango de fecha
            if null_q[1]:
                ais = ais.filter(BaseDateTime__range=(date_from, date_to))
                plate = plate.filter(
                    Fecha_Inicio__range=(date_from, date_to),
                    Fecha_Fin__range=(date_from, date_to),
                )
                ais_ids = ais.values_list("MMSI", flat=True)
                vessel = vessel.filter(MMSI__in=ais_ids)
        elif i == 3 and notNull:
            # Busquedad en base a la talla del pez
            lote_ids = Fish_Plate.objects.filter(
                Lote__in=Plate.objects.filter(Matricula__in=vessel), Talla_cm=talla
            ).values_list("Lote", flat=True)
            vessel = vessel.filter(
                Matricula__in=Plate.objects.filter(Lote__in=lote_ids).values_list(
                    "Matricula", flat=True
                )
            )
            ais = ais.filter(MMSI__in=vessel)
        elif i == 4 and notNull:
            # Busquedad en base al nombre comercial del pez
            fish = Fish.objects.filter(Nombre_Comercial__startswith=pez)
            lote_ids = Fish_Plate.objects.filter(
                Lote__in=Plate.objects.filter(Matricula__in=vessel),
                Nombre_Cientifico__in=fish,
            ).values_list("Lote", flat=True)
            vessel = vessel.filter(
                Matricula__in=Plate.objects.filter(Lote__in=lote_ids).values_list(
                    "Matricula", flat=True
                )
            )
            ais = ais.filter(MMSI__in=vessel)
        elif (null_q[1] and not null_q[2]) or (not null_q[1] and null_q[2]):
            raise DateRangeException
    return vessel, ais


def Filter_Type(TypeStr, v, ais):
    """
    Simple filter and selection of collections and route by type we want to choose
    Input: String
    Output: FeatureCollection, String, String
    """
    route = "webgisapp/maproute_search.html"
    if TypeStr == "Line":
        collection = AISQuery_To_Collection(v, ais, LineString)
        typee = "line"
    elif TypeStr == "Point":
        collection = AISQuery_To_Collection(v, ais, MultiPoint)
        typee = "circle"
    elif TypeStr == "PointAndLine":
        collection = AISQuery_To_Collection(v, ais, LineString)
        typee = "pointandline"
    elif TypeStr == "Heat":
        collection = AISQuery_To_Collection(v, ais, MultiPoint, True)
        typee = "heat"
        route = "webgisapp/maproutes/heat.html"
    elif TypeStr is not None and not isinstance(TypeStr, str):
        raise InstanceTypeException
    elif TypeStr is None or len(TypeStr) == 0:
        raise EmptyVarException
    else:
        raise IncorrectOptionException
    return collection, route, typee
