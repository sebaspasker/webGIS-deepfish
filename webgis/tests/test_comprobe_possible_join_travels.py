import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTestDeleteTravel
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.join_travel import Delete_None_Existing_Travels

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestDeleteTravel:
    pytestmark = pytest.mark.django_db

    def setup(self):
        setupTestComprobePossibleJoin(self)

    def AISCorrectType(self):
        # TODO
        pass

    def VesselCorrectType(self):
        # TODO
        pass

    def PlateCorrectType(self):
        # TODO
        pass

    def AISQuerySetCorrectType(self):
        # TODO
        pass

    def VesselQuerySetCorrectType(self):
        # TODO
        pass

    def PlateQuerySetCorrectType(self):
        # TODO
        pass

    # TODO mas pruebas una vez que se utilze para alguna implementación
