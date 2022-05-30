from calendar import c

from numpy import true_divide
import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupComprobePossibleJoinTravel
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.join_travel import Comprobe_Possible_Join_Travels

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestJoinTravel:
    pytestmark = pytest.mark.django_db

    def setup(self):
        setupComprobePossibleJoinTravel(self) 

    def testOnlyJoinOneAIS(self):
        ais = AISVessel.objects.filter(VesselName="Jorge")
        assert False == Comprobe_Possible_Join_Travels(aiss=ais)
        esta_jorge = False
        for travel in Travel.objects.all():
            if travel.AIS_fk.VesselName == "Jorge":
                esta_jorge = True

        assert esta_jorge == True, "Debería de dar True porque Jorge está en la base de datos de travels"

    def testOnlyJoinOneVessel(self):
        ves = Vessel.objects.filter(VesselName="Juan")
        assert False == Comprobe_Possible_Join_Travels(vessels=ves)
        esta_juan = False
        for travel in Travel.objects.all():
            if travel.Vessel_fk.VesselName == "Juan":
                esta_juan = True

        assert esta_juan == True, "Debería de dar True porque Juan está en la base de datos de travels"
        

    def testOnlyJoinOnePlate(self):
        plat=Plate.objects.filter(Matricula=self.v1)
        assert False == Comprobe_Possible_Join_Travels(plates=plat)
        esta_plate = False
        for travel in Travel.objects.all():
            if travel.Plate_fk.Matricula.VesselName == "Juan":
                esta_plate = True
        
        assert esta_plate == True, "Debería de dar True porque Juan está en la base de datos de travels"








