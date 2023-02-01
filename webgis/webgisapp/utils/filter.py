from webgisapp.models import *
from .ais_to_geojson import AISQuery_To_Collection
from .exceptions import *
from geojson import LineString, Point, MultiPoint
import datetime


def Filter_Route(
    MMSI=None, date_from=None, date_to=None, talla=None, pez=None, posicion=None
):
    """
    Comprueba los objetos que no estén vaciós de las variables:
        MMSI, fecha inicio, fecha fin, talla, pez
    Y mete un filtrado en la base de datos en base a esos parámetros.
    """
    null_q = []
    for var in [
        MMSI,
        date_from,
        date_to,
        talla,
        pez,
        posicion,
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
    for notNull, i in zip(null_q, range(6)):  # Filtrado
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
                Plate__in=Plate.objects.filter(Matricula__in=vessel),
                Talla_cm__gt=float(talla),
                Talla_cm__lt=float(talla) + 1.0,
            ).values_list("Plate_id", flat=True)
            plates = Plate.objects.filter(Id__in=lote_ids).values_list(
                "Matricula", flat=True
            )

            vessel = vessel.filter(Matricula__in=plates)
            ais = ais.filter(MMSI__in=vessel)
        elif i == 4 and notNull:
            # Busquedad en base al nombre comercial del pez
            fish = Fish.objects.filter(Nombre_Cientifico__contains=pez)
            lote_ids = Fish_Plate.objects.filter(
                Plate__in=Plate.objects.filter(Matricula__in=vessel),
                Nombre_Cientifico__in=fish,
            ).values_list("Plate_id", flat=True)
            vessel = vessel.filter(
                Matricula__in=Plate.objects.filter(Id__in=lote_ids).values_list(
                    "Matricula", flat=True
                )
            )
            ais = ais.filter(MMSI__in=vessel)
        elif i == 5 and notNull:
            lon, lat = map(float, posicion.split(","))
            ais = ais.filter(
                LON__gt=lon - 0.02,
                LON__lt=lon + 0.02,
                LAT__gt=lat - 0.02,
                LAT__lt=lat + 0.02,
            )
            vessel = vessel.filter()
            ais_ids = ais.values_list("MMSI", flat=True)
            vessel = vessel.filter(MMSI__in=ais_ids)
        elif (null_q[1] and not null_q[2]) or (not null_q[1] and null_q[2]):
            raise DateRangeException
    return vessel, ais


def Filter_Type(TypeStr, v, ais):
    """
    Simple filter and selection of collections and route by type we want to choose
    Input: String
    Output: FeatureCollection, String, String
    """
    route = "webgisapp/map/map_index.html"
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
        collection = AISQuery_To_Collection(v, ais, MultiPoint, True, True)
        typee = "heat"
        route = "webgisapp/map/map_index.html"
    elif TypeStr is not None and not isinstance(TypeStr, str):
        raise InstanceTypeException
    elif TypeStr is None or len(TypeStr) == 0:
        raise EmptyVarException
    else:
        raise IncorrectOptionException
    return collection, route, typee


def filterDictForm(dictform):
    mmsi = None
    date_from = None
    date_to = None
    talla = None
    especie = None
    posicion = None
    for i in range(1, 7):
        text_input = dictform["text_input_" + str(i)]
        if not "".__eq__(text_input):
            option = dictform["option_" + str(i)]
            if option == "mmsi":
                mmsi = text_input
            elif option == "fecha_inicio":
                date_from = text_input
            elif option == "fecha_fin":
                date_to = text_input
            elif option == "talla":
                talla = text_input
            elif option == "especie":
                especie = text_input
            elif option == "posicion":
                posicion = text_input
    return mmsi, date_from, date_to, talla, especie, posicion
