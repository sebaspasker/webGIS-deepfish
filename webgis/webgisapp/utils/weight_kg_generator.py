from webgisapp.models import *

class EmptySpecieException(Exception):
    """Exception for error when specie is empty"""
    def __init__(self,message="Name specie is empty"):
        super().__init__(self.message)

def relateAISKg(travels, specie=False, name_specie=""):
    travel_kg = {}
    for travel in travels:
        ais = travel.AIS_fk
        plate = travel.Plate_fk
        avg = 0.0
        if not specie:
            fish_plates = Fish_Plate.objects.filter(Lote=plate)
        else:
            if not "".__eq__(name_specie):
                fish_plates = Fish_Plate.objects.filter(Lote=plate, 
                                        Nombre_Cientifico__in=Fish.objects.filter(Nombre_Cientifico=name_specie))
            else:
                raise EmptySpecieException
        if len(fish_plates) > 0:
            for fish_plate in fish_plates:
                # print(fish_plate)
                avg += fish_plate.Peso
            avg = avg/len(fish_plates)
            travel_kg[travel.id] = {'travel' : travel, 'Kg' : avg}

    return travel_kg
