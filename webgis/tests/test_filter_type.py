import pytest
import datetime
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupFilterType
from webgisapp.utils.exceptions import *
from webgisapp.utils.abbr import *
from webgisapp.utils.filter import Filter_Type, Filter_Route

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestFilterType:
    pytestmark = pytest.mark.django_db
    collection = ""

    # Input: TypeStr, Vessels, AIS
    # Ouput: collection, route, typee

    def setup(self):
        setupFilterType(self)

    def testStrEmpty(self):
        try:
            Filter_Type("", allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, EmptyVarException)

    def testStrDifferent(self):
        try:
            Filter_Type("Random", allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, IncorrectOptionException)

    def testNotVessel(self):
        try:
            Filter_Type("Point", "", allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, InstanceTypeException)

    def testNotAIS(self):
        try:
            Filter_Type("Point", allVessels(), "")
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, InstanceTypeException)

    def testPointType(self):
        correct_route = "webgisapp/maproute_search.html"
        correct_type = "circle"
        collection, route, typee = Filter_Type("Point", allVessels(), allAIS())
        assert collection == self.collection, "Different Collection"
        assert route == correct_route, "Different route"
        assert typee == correct_type, "Different type"

    def testLineStringType(self):
        correct_route = "webgisapp/maproute_search.html"
        correct_type = "line"
        collection, route, typee = Filter_Type("Line", allVessels(), allAIS())
        assert collection == self.collection2, "Different Collection"
        assert route == correct_route, "Different Route"
        assert typee == correct_type, "Different Type"

    def testPointAndLineType(self):
        correct_route = "webgisapp/maproute_search.html"
        correct_type = "pointandline"
        collection, route, typee = Filter_Type("PointAndLine", allVessels(), allAIS())
        assert collection == self.collection2, "Different Collection"
        assert route == correct_route, "Different Route"
        assert typee == correct_type, "Different Type"

    def testHeatType(self):
        correct_route = "webgisapp/maproutes/heat.html"
        correct_type = "heat"
        collection, route, typee = Filter_Type("Heat", allVessels(), allAIS())

        assert collection == self.collection3, "Different Collection"
        assert route == correct_route, "Different Route"
        assert typee == correct_type, "Different Type"
