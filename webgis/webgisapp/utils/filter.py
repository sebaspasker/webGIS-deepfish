from webgisapp.models import *
import datetime

def Filter_Route(MMSI, date_from, date_to, talla, pez):
    """
    Comprueba los objetos que no estén vaciós de las variables:
        MMSI, fecha inicio, fecha fin, talla, pez
    Y mete un filtrado en la base de datos en base a esos parámetros.
    """
    null_q = []
    for var in [MMSI, date_from, date_to, talla, pez]:
        if var is None:
            null_q.append(False)
        elif isinstance(var, str) and ''.__eq__(var):
            null_q.append(False)
        else:
            null_q.append(True)

    ais = AISVessel.objects.all()
    vessel = Vessel.objects.all()
    plate = Plate.objects.all()
    for notNull, i in zip(null_q, range(5)):
        if i == 0 and notNull:
            vessel = vessel.filter(MMSI__contains=MMSI)
            ais = ais.filter(MMSI__in=vessel)
        elif i == 2 and notNull:
            if null_q[1]:
                ais = ais.filter(BaseDateTime__range=(date_from, date_to))
                plate = plate.filter(Fecha_Inicio__range=(date_from, date_to), Fecha_Fin__range=(date_from, date_to))
        elif i == 3 and notNull:
            lote_ids = Fish_Plate.objects.filter(Lote__in=Plate.objects.filter(Matricula__in=vessel),
                                                 Talla_cm=talla).values_list('Lote', flat=True)
            vessel = vessel.filter(Matricula__in=Plate.objects.filter(Lote__in=lote_ids).values_list('Matricula',flat=True))
        elif i == 4 and notNull:
            fish = Fish.objects.filter(Nombre_Comercial__startswith=pez)
            lote_ids = Fish_Plate.objects.filter(Lote__in=Plate.objects.filter(Matricula__in=vessel),
                                                 Nombre_Cientifico__in=fish).values_list('Lote', flat=True)
            vessel = vessel.filter(Matricula__in=Plate.objects.filter(Lote__in=lote_ids).values_list('Matricula', flat=True))
            ais = ais.filter(MMSI__in=vessel)
    return vessel, ais
