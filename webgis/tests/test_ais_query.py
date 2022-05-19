import datetime
import pytest
from webgisapp.utils.ais_to_geojson import AISQuery_To_Collection
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
# from webgisapp.models import AISVessel, Vessel
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
import random


pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestAISQuery:
    pytestmark = pytest.mark.django_db
    collection = ""
    collection2 = ""

    def setup(self):
        v1 = Vessel.objects.create(
            MMSI = "123456789",
            VesselName="Juan",
            Matricula="M123"
        )

        v2 = Vessel.objects.create(
            MMSI = "987654321",
            VesselName="Jorge",
            Matricula="A321"
        )

        ais1 = AISVessel.objects.create(
            MMSI = v1,
            BaseDateTime = datetime.datetime.now(),
            LAT=1,
            LON=1,
            SOG=1,
            COG=1,
            VesselName=v1.VesselName,
            CallSign='ABC',
            VesselType=1,
            Status=1,
             Length=1,
            Width=1,
            Cargo=1,
            TransceiverClass='A'
        )

        ais2 = AISVessel.objects.create(
            MMSI = v2,
            BaseDateTime = datetime.datetime.now(),
            LAT=1,
            LON=1,
            SOG=1,
            COG=1,
            VesselName=v1.VesselName,
            CallSign='ABC',
            VesselType=1,
            Status=1,
            Length=1,
            Width=1,
            Cargo=1,
            TransceiverClass='A'
        )

        self.collection = FeatureCollection(
            [
                Feature(
                    geometry = Point([(ais1.LON, ais1.LAT)]),
                    properties = {
                        'MMSI': v1.MMSI,
                        'VesselName' : v1.VesselName,
                        'Matricula' : v1.Matricula,
                        'Color' : "#fe0000", # Red
                    }),
                Feature(
                    geometry = Point([(ais2.LON, ais2.LAT)]),
                    properties = {
                        'MMSI': v2.MMSI,
                        'VesselName' : v2.VesselName,
                        'Matricula' : v2.Matricula,
                        'Color' : "#fe4600", # Red Orange
                }),
            ]
            )

        self.collection2 = FeatureCollection(
            [
                Feature(
                    geometry = Point([(float(ais1.LON), float(ais1.LAT))]),
                    properties = {
                        'MMSI': v1.MMSI,
                        'VesselName' : v1.VesselName,
                        'Matricula' : v1.Matricula,
                        'Color' : "#fe0000", # Red
                    }),
                Feature(
                    geometry = Point([(float(ais2.LON), float(ais2.LAT))]),
                    properties = {
                        'MMSI': v2.MMSI,
                        'VesselName' : v2.VesselName,
                        'Matricula' : v2.Matricula,
                        'Color' : "#fe4600", # Red Orange
                }),
            ]
            )

            
    def test_VesselEmpty(self): 
        try:
            AISQuery_To_Collection(
                None,
                allAIS(),
                Point,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, EmptyVarException) == True

    def testAISEmpty(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                None,
                Point,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, EmptyVarException) == True


    def testTypeEmpty(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                allAIS(),
                None,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, EmptyVarException) == True

    def testHeatEmpty(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                allAIS(),
                Point,
                Heat=None,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, EmptyVarException) == True

    def testNotVesselType(self):
        try:
            AISQuery_To_Collection(
                "",
                allAIS(),
                Point,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, InstanceTypeException) == True

    def testNotAISType(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                "",
                Point,
                )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, InstanceTypeException) == True

    def testNotGeojsonType(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                allAIS(),
                "",
                )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, InstanceTypeException) == True

    def testHeatNotType(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                allAIS(),
                Point,
                Heat="")
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, InstanceTypeException) == True

    def testVesselsDiferentQuery(self):
        try:
            AISQuery_To_Collection(
                allAIS(),
                allAIS(),
                Point,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, QueryTypeException) == True

    def testAISDiferentQuery(self):
        try:
            AISQuery_To_Collection(
                allVessels(),
                allVessels(),
                Point,
            )
            assert False, "Should have an exception"
        except Exception as e:
            assert isinstance(e, QueryTypeException) == True

    def testHeatTrue(self):
        result = AISQuery_To_Collection(
            allVessels(),
            allAIS(),
            Point,
            Heat=True
        )
        assert result == self.collection, "Diferente colección"

    def testHeatFalse(self):
        result = AISQuery_To_Collection(
            allVessels(),
            allAIS(),
            Point,
            Heat=False
        )
        assert result == self.collection2

# def testHeatType(self):
#     # TODO
#     self.fail("No creado el test")
#     pass

# def testHeatEmptyVessel(self):
#     # TODO
#     self.fail("No creado el test")
#     pass

# def testNotHeatEmptyVessel(self):
#     # TODO
#     self.fail("No creado el test")
#     pass

# def testHeatEmptyAIS(self):
#     # TODO
#     self.fail("No creado el test")
#     pass

# def testNotHeatEmptyAIS(self):
#     # TODO
#     self.fail("No creado el test")
#     pass
