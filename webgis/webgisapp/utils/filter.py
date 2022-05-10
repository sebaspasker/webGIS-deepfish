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
            print("FIRST ", vessel, ais)
        elif i == 2 and notNull:
            if null_q[1]:
                ais = ais.filter(BaseDateTime__range=(date_from, date_to))
                plate = plate.filter(Fecha_Inicio__range=(date_from, date_to), Fecha_Fin__range=(date_from, date_to))
            print("SECOND ", vessel, ais)
        elif i == 3 and notNull:
            plates = Plate.objects.filter(Matricula__in=vessel) 
            # fish_plates = Fish_Plate.objects.filter(Lote__in=plates, Talla_cm__contains=talla)
            fish_plates = Fish_Plate.objects.filter(Lote__in=plates, Talla_cm=talla)
            lote_ids = Fish_Plate.objects.filter(Lote__in=plates, Talla_cm=talla).values_list('Lote', flat=True)
            vessel = vessel.filter(Matricula__in=Plate.objects.filter(Lote__in=lote_ids).values_list('Matricula',flat=True))
            # plates = fish_plates[0].LoteOf.all()
            print("THIRD ", vessel, ais, fish_plates, plates)
        elif i == 4 and notNull:
            fish = Fish.objects.filter(Nombre_Comercial__contains=pez)
            if not null_q[3]:
                plates = Plate.objects.filter(Matricula__in=vessel) 
            fish_plates = Fish_Plate.objects.filter(Lote__in=plates, Nombre_Cientifico__in = fish)
            plates = plates.filter(Lote__in=fish_plates)
            vessel = vessel.filter(Matricula__in=plates)
            ais = ais.filter(MMSI__in=vessel)
            print("FOURTH ", vessel, ais, fish, plates, fish_plates)
    return vessel, ais
