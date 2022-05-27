import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTestComprobeOutdatedTravel
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.join_travel import Delete_None_Existing_Travels

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestComprobeOutdatedTravel:
    pytestmark = pytest.mark.django_db

    def setup(self):
        setupTestComprobeOutdatedTravel(self)

    def testNotOutdated(self):
        # TODO debería de devolver un falso si está actualizado
        assert TestComprobeOutdatedTravel() == False

    def testEmptyOutdated(self):
        for travel in Travel.objects.all():
            travel.delete()
        assert Comprobe_Outdated_Travels() == True

    def testOutdated(self):
        # TODO
        pass

    def testAISOutdated(self):
        # TODO
        pass

    def testVesselOutdated(self):
        # TODO
        pass

    def testPlateOutdated(self):
        # TODO
        pass

    def selectiveOutdatedTravels(self):
        # TODO
        pass

    pass
