from webgisapp.models import *
from .join_travel import Comprobe_Outdated_Travels, Delete_None_Existing_Travels
from .exceptions import *
import time
import numpy as np


def relateAISKg(travels, specie=False, name_specie=""):
    start_time = time.time()
    #if Comprobe_Outdated_Travels(travels):
    #    Delete_None_Existing_Travels(travels)
    print("--- %s seconds --- line Comprobe_Outdated_Travels" % (time.time() - start_time))
    travel_kg = {}
    i = 0
    
    travels2 = np.array(travels)
    print("travels2_len: ", len(travels2))
    i = 0
    for travel in travels2:
        i+=1
        ais = travel.AIS_fk
        plate = travel.Plate_fk
        avg = 0.0
        if not specie:
            fish_plates = Fish_Plate.objects.filter(Plate=plate)
            # fish_plates = Fish_Plate.objects.all()
        else:
            if not "".__eq__(name_specie):
                fish_plates = Fish_Plate.objects.filter(
                    Lote=plate,
                    Nombre_Cientifico__in=Fish.objects.filter(
                        Nombre_Cientifico=name_specie
                    ),
                )
            else:
                raise EmptySpecieException
        if len(fish_plates) > 0:
            for fish_plate in fish_plates:
                # print(fish_plate)
                avg += fish_plate.Peso
            avg = avg / len(fish_plates)
            travel_kg[travel.id] = {"Kg": avg}
        else:
            travel_kg[travel.id] = {"Kg": 0.0}
        
        if i%1000 == 0:
            print(i)
            
    print("travel_kg")
    print(travel_kg)
    return travel_kg
