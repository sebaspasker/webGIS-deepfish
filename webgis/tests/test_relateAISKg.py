from calendar import c
from queue import Empty

from numpy import true_divide
import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupRelateAISKg
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.weight_kg_generator import relateAISKg

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestRelateAISKg:
    pytestmark = pytest.mark.django_db

    def setup(self): 
        setupRelateAISKg(self) 

    def testVesselExists(self):
        ves = Vessel.objects.filter(VesselName="Juan")
        esta_juan = False
        for travel in Travel.objects.all():
            if travel.Vessel_fk.VesselName == "Juan":
                esta_juan = True

        assert esta_juan == True, "Debería de dar True porque Juan está en la base de datos de travels"

    def testAISExists(self):
        ais = AISVessel.objects.filter(VesselName="Juan")
        esta_jorge = False
        for travel in Travel.objects.all():
            if travel.AIS_fk.VesselName == "Juan":
                esta_jorge = True

        assert esta_jorge == True, "Debería de dar True porque el AIS asoTciado a Jorge está en la base de datos de travels"

    def testPlateExists(self):
        plat=Plate.objects.filter(Matricula=self.v1)
        esta_plate = False
        for travel in Travel.objects.all():
            if travel.Plate_fk.Matricula.VesselName == "Juan":
                esta_plate = True
        
        assert esta_plate == True, "Debería de dar True porque Juan está en la base de datos de travels"

    def testFishExists(self):
        pezfi=Fish.objects.filter(Nombre_Cientifico="Pez1")
        esta_fish = False
        for fplate in Fish_Plate.objects.all():
            if fplate.Nombre_Cientifico.Nombre_Cientifico == "Pez1":
                esta_fish = True

        assert esta_fish == True, "Debería de dar True porque Pez1 existe en la base de datos"


    def testFishPlateExists(self):
        # Esta mal, devuelve un diccionario
        fishplat = Fish_Plate.objects.filter(Nombre_Cientifico = self.p)
        assert len(fishplat) > 0
        assert fishplat[0], "Debería dar True porque existe al menos 1 pez en la base de datos con esa info"


    def testTravelExists(self):
        """
        EL IF ESE ES PARA COMPROBAR QUE TANTO EL VESSEL 
        COMO EL AIS COMO EL PLATE PERTENECEN TODOS AL MISMO TRAVEL
        """
        travels = Travel.objects.all()
        esta_Travel = False
        for travel in travels:
            if travel.Vessel_fk.VesselName == "Juan" and travel.AIS_fk.VesselName == "Juan" and travel.Plate_fk.Matricula.VesselName == "Juan":
                esta_Travel = True

        assert esta_Travel == True, "Debería de dar True porque los datos están en la base de datos de travels"


# Esta función relateAISKg pilla unos viajes
# Viaje : Vessel, AIS, Plate (Bandeja)
# Plate 1--N FishPlates
# FishPlates Especie, Kg
# Travel --> AIS (coordenadas) -- relacionado con -- Barco (Vessel)
# Plate -- relacionado con -- Barco
# AIS (ais) -- relacionado con -- Vessel -- Relaciodo con -- Plate (kg)
# Devuelve un diccionario {"Travel" : [(AIS, Vessel, Plate) : KG]}

    def testTravelEmptyInRelate(self):
        # Comprueba que salte una excepción si está 
        # vacío los travels
        try:
            relateAISKg(
                specie=True, name_specie="Pez1"
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"
        

    def testSpecieTruePeroName_SpecieEmpty(self):
        alltravels = Travel.objects.all()
        try:
            relateAISKg(
                travels = alltravels, specie=True
            )
        except Exception as e:
            assert isinstance(
                e, EmptySpecieException
            ), "Debería de saltar EmptySpecieException"

# Setup Pez: "pez1", vessel: "barco1", ais: "ais1", plate: "plate1" -> 3*fishplate: "fishplate" -> "pez1" y 3
# Creas dos travels relacionados fish plates
# Travel(barco1, ais1, plate1)
# Corres la funcion
# dict -> return -> {travel.id : 9.0}. fishplate[travel.id] -> kg 
# assert fishplate[travel.id] == 9.0

# Crear una funcion con un travel
# Una función con dos travels

# funcion(Travels.objects.all())
# function(Travels.objects.all()[0])

# Travel con ningun plate relacionado

# TRAVEL1 ESTA RELACIONADO CON UN FISHPLATE
# TRAVEL2 NO ESTA RELACIONADO CON UN FISHPLATE
# TRAVEL 3 ESTA RELACIONADO CON 2 FISHPLATES, UNO DE 5 Y OTRO DE 15
    def testTravelKg(self):
        travelList = Travel.objects.all()
        diccionario = relateAISKg(travels=travelList)
        minidic1 = diccionario[travelList[0].id]
        assert minidic1["Kg"]==3
        minidic2 = diccionario[travelList[1].id]
        assert minidic2["Kg"]==0  
        minidic3 = diccionario[travelList[2].id]
        assert minidic3["Kg"]==10  
        
        









