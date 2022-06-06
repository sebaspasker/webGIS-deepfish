from .abbr import *
from django.db.models.query import QuerySet
from .exceptions import *
from webgisapp.models import *


def Join_Travels(vessels=None, aiss=None, plates=None):
    """
    Automatización para crear una triple relación entre los barcos, las bandejas y
    los ais y subirlo a la tabla de Travels.
    """
    if vessels is None:
        vessels = Vessel.objects.all()
    if aiss is None:
        aiss = AISVessel.objects.all()
    if plates is None:
        plates = Plate.objects.all()
    comprobation_type(vessels, aiss, plates)

    for vessel in vessels:
        aisss = aiss.filter(MMSI=vessel)  # FIltramos ais en base al vessel
        for ais in aisss:
            platess = plates.filter(
                Matricula=vessel,  # Filtramos bandejas en base al vessel y fecha ais
                Fecha_Inicio__lt=ais.BaseDateTime,
                Fecha_Fin__gt=ais.BaseDateTime,
            )
            for plate in platess:
                travel = Travel(
                    Vessel_fk=vessel, AIS_fk=ais, Plate_fk=plate
                )  # Relacionamos
                try:
                    travel.save()
                except Exception as e:
                    print(e)


def Delete_None_Existing_Travels(travels=None):
    """
    Elimina los viajes en los que ya no existe relación.
    """
    if travels is None:
        travels = Travel.objects.all()
    vessels = Vessel.objects.all()
    ais = AISVessel.objects.all()
    plates = Plate.objects.all()
    for travel in travels:
        if (
            travel.AIS_fk not in ais
            or travel.Vessel_fk not in vessels
            or travel.Plate_fk not in plates
        ):
            travel.delete()


# TODO probar correcto funcionamiento
def Comprobe_Outdated_Travels(travels=None):
    """
    Comprueba si los viajes están desactualizados.
    """
    if travels is None:
        travels = Travel.objects.all()
    vessels = Vessel.objects.all()
    ais = AISVessel.objects.all()
    plates = Plate.objects.all()
    for travel in travels:
        if (
            travel.AIS_fk not in ais
            or travel.Vessel_fk not in vessels
            or travel.Plate_fk not in plates
        ):
            return True
    return False


# De momento no se utiliza
def Comprobe_Possible_Join_Travels(ais=None, plates=None, vessels=None):
    """
    Comprueba si existen viajes existentes sin añadir a la base de datos y los guarda.
    """
    if ais is None:
        ais = allAIS()
    if plates is None:
        plates = allPlates()
    if vessels is None:
        vessels = allVessels()

    travels = Travel.objects.all()
    for vessel in vessels:
        aiss = ais.filter(MMSI=vessel)
        platess = plates.filter(Matricula=vessel.Matricula)
        for ais_obj in aiss:
            for plate in platess:
                try:
                    t = Travel(Vessel_fk=vessel, Plate_fk=plate, AIS_fk=ais)
                    t.save()
                except Exception as e:
                    return True
    return False


def comprobation_type(vessels, aiss, plates):
    if (
        not isinstance(vessels, QuerySet)
        or not isinstance(aiss, QuerySet)
        or not isinstance(plates, QuerySet)
    ):
        raise InstanceTypeException
    elif (
        (len(vessels) > 0 and not isinstance(vessels[0], Vessel))
        or (len(aiss) > 0 and not isinstance(aiss[0], AISVessel))
        or (len(plates) > 0 and not isinstance(plates[0], Plate))
    ):
        raise QueryTypeException
