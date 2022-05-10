from webgisapp.models import *

def Join_Travels():
    """
    Automatización para crear una triple relación entre los barcos, las bandejas y 
    los ais y subirlo a la tabla de Travels
    """
    vessels = Vessel.objects.all()
    for vessel in vessels:
        aiss = AISVessel.objects.filter(MMSI=vessel) # FIltramos ais en base al vessel
        for ais in aiss:
            plates = Plate.objects.filter(Matricula=vessel,  # Filtramos bandejas en base al vessel y fecha ais
                                         Fecha_Inicio__lt=ais.BaseDateTime, Fecha_Fin__gt=ais.BaseDateTime)
            for plate in plates:
                travel = Travel(Vessel_fk=vessel, AIS_fk=ais, Plate_fk=plate) # Relacionamos
                travel.save()
            


