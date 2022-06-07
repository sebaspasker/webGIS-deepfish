import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTestDeleteTravel
from .setups import setupTestComprobeOutdatedTravel
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.join_travel import Delete_None_Existing_Travels

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestDeleteTravel:
    pytestmark = pytest.mark.django_db

    def setup(self):
        setupTestDeleteTravel(self)

    def testDeleteAllDB(self):
        for ais in AISVessel.objects.all():
            ais.delete()
        for vessel in Vessel.objects.all():
            vessel.delete()
        for plate in Plate.objects.all():
            plate.delete()
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 0

    def testDeleteAllAIS(self):
        for ais in AISVessel.objects.all():
            ais.delete()
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 0

    def testDeleteAllVessel(self):
        for vessel in Vessel.objects.all():
            vessel.delete()
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 0

    def testDeleteAllPlates(self):
        for plate in Plate.objects.all():
            plate.delete()
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 0

    def testDeleteOnlyOneRelation(self):
        AISVessel.objects.all()[0].delete()
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 1

    def testDeleteOnlyOneTravelInput(self):
        ais = AISVessel.objects.all()[0]
        travel = Travel.objects.filter(AIS_fk=ais)
        ais.delete()
        Delete_None_Existing_Travels(Travel.objects.filter(AIS_fk=ais))
        assert len(Travel.objects.all()) == 1

    def testDeleteNoneTravel(self):
        Delete_None_Existing_Travels()
        assert len(Travel.objects.all()) == 2


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
