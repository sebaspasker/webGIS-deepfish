from webgisapp.models import *
from .join_travel import Comprobe_Outdated_Travels, Delete_None_Existing_Travels
from .exceptions import *

def relateAISKg(travels, specie=False, name_specie=""):
    if Comprobe_Outdated_Travels(travels):
        Delete_None_Existing_Travels(travels)
    travel_kg = {}
    for travel in travels:
        ais = travel.AIS_fk
        plate = travel.Plate_fk
        avg = 0.0
        if not specie:
            fish_plates = Fish_Plate.objects.filter(Lote=plate)
            # fish_plates = Fish_Plate.objects.all()
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
        else:
            travel_kg[travel.id] = {'travel' : travel, 'Kg' : 0.0}

    return travel_kg
