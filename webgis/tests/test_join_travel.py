import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTestJoinTravel
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.join_travel import Join_Travels

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestJoinTravel:
    pytestmark = pytest.mark.django_db

    def setup(self):
        setupTestJoinTravel(self)

    def testOnlyJoinOneAIS(self):
        Join_Travels(aiss=AISVessel.objects.filter(VesselName="Jorge"))
        travel = Travel.objects.all()[0]
        assert len(Travel.objects.all()) == 1
        assert travel.AIS_fk == self.ais2
        assert travel.Vessel_fk == self.v2
        assert travel.Plate_fk == self.plate2

    def testOnlyJoinOneVessel(self):
        Join_Travels(vessels=Vessel.objects.filter(VesselName="Juan"))
        travel = Travel.objects.all()[0]
        assert len(Travel.objects.all()) == 1
        assert travel.AIS_fk == self.ais1
        assert travel.Vessel_fk == self.v1
        assert travel.Plate_fk == self.plate1

    def testOnlyJoinOnePlate(self):
        Join_Travels(plates=Plate.objects.filter(Matricula=self.v1))
        travel = Travel.objects.all()[0]
        assert len(Travel.objects.all()) == 1
        assert travel.AIS_fk == self.ais1
        assert travel.Vessel_fk == self.v1
        assert travel.Plate_fk == self.plate1

    def testAllJoinTravel(self):
        Join_Travels()
        travels = Travel.objects.all()
        assert len(travels) == 2
        travel1 = travels[0]
        travel2 = travels[1]
        assert travel1.AIS_fk == self.ais1
        assert travel1.Vessel_fk == self.v1
        assert travel1.Plate_fk == self.plate1
        assert travel2.AIS_fk == self.ais2
        assert travel2.Vessel_fk == self.v2
        assert travel2.Plate_fk == self.plate2

    def testAISDifferenteType(self):
        try:
            Join_Travels(aiss="str")
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, InstanceTypeException
            ), "Debería de saltar InstanceTypeException"

    def testVesselDifferentType(self):
        try:
            Join_Travels(vessels="str")
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, InstanceTypeException
            ), "Debería de saltar InstanceTypeException"

    def testPlateDiferentType(self):
        try:
            Join_Travels(plates="str")
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, InstanceTypeException
            ), "Debería de saltar InstanceTypeException"

    def testAISDifferentQuery(self):
        try:
            Join_Travels(aiss=allVessels())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, QueryTypeException
            ), "Debería de saltar QueryTypeException"

    def testVesselDifferentQuery(self):
        try:
            Join_Travels(vessels=allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, QueryTypeException
            ), "Debería de saltar QueryTypeException"

    def testPlateDifferentQuery(self):
        try:
            Join_Travels(plates=allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, QueryTypeException
            ), "Debería de saltar QueryTypeException"
