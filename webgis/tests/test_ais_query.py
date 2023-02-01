import datetime
import pytest
import random
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTestAISQuery
from webgisapp.utils.ais_to_geojson import AISQuery_To_Collection
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *

# from webgisapp.models import AISVessel, Vessel


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestAISQuery:
    pytestmark = pytest.mark.django_db
    collection = ""
    collection2 = ""

    def setup(self):
        setupTestAISQuery(self)

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
            AISQuery_To_Collection(allVessels(), allAIS(), Point, Heat="")
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
        result = AISQuery_To_Collection(allVessels(), allAIS(), Point, Heat=True)
        assert result == self.collection, "Diferente colección"

    def testHeatFalse(self):
        result = AISQuery_To_Collection(allVessels(), allAIS(), Point, Heat=False)
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
