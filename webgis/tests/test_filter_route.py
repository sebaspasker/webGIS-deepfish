from datetime import datetime, timedelta
import pytest
from geojson import Point, LineString, MultiPoint
from .setups import setupFilterRoute
from webgisapp.utils.exceptions import *
from webgisapp.utils.abbr import *
from webgisapp.utils.filter import Filter_Type, Filter_Route
from webgisapp.models import *

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestFilterRoute:
    pytestmark = pytest.mark.django_db

    # Input: MMSI, date_from, date_to, talla, pez
    # Output: Vessel, ais
    def setup(self):
        setupFilterRoute(self)

    def testMMSIEmpty(self):
        try:
            vessel, ais = Filter_Route("", datetime.now(), datetime.now(), 1, self.p)
            assert False, "Should launch an exception"
        except Exception as e:
            assert isinstance(e, EmptyVarException), "Incorrect Exception"

    def testMMSIExist(self):
        vessel, ais = Filter_Route(
            "ABCDEF",
        )
        assert len(vessel) != 0

    def testMMSIDontExist(self):
        vessel, ais = Filter_Route(
            "FSDSD",
        )

        assert len(vessel) == 0

    def testDateInDB(self):
        vessel, ais = Filter_Route(
            date_from=datetime.now() - timedelta(minutes=5),
            date_to=datetime.now() + timedelta(minutes=5),
        )

        assert self.v == vessel[0], "Not same vessel"
        assert self.ais1 == ais[0], "Not same AIS"
        assert self.ais2 == ais[1], "Not same AIS"

    def testDateNotInDB(self):
        vessel, ais = Filter_Route(
            date_from=datetime.now() - timedelta(days=2),
            date_to=datetime.now() - timedelta(days=1),
        )

        assert len(ais) == 0, "Tamaño de ais debería de ser 0"
        assert len(vessel) == 0, "Tamaño de vessel debería de ser 0"

    def testTallaInDB(self):
        vessel, ais = Filter_Route(
            talla=2,
        )

        assert len(ais) == 2, "Tamaño de ais debería de ser 2"
        assert len(vessel) == 1, "Tamaño de vessel debería de ser 1"

    def testTallaNotInDB(self):
        vessel, ais = Filter_Route(
            talla=4,
        )

        assert len(ais) == 0, "Tamaño de ais debería de ser 0"
        assert len(vessel) == 0, "Tamaño de vessel debería de ser 0"

    def testDateFromEmpty(self):
        try:
            vessel, ais = Filter_Route(date_from=None, date_to=datetime.now())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, DateRangeException
            ), "Debería ser excepción de tipo DateRangeException"

    def testDateToEmpty(self):
        try:
            vessel, ais = Filter_Route(
                date_from=datetime.now(),
                date_to=None,
            )
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, DateRangeException
            ), "Debería ser excepción de tipo DateRangeException"

    def testPezEmpty(self):
        try:
            vessel, ais = Filter_Route(
                pez="",
            )
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(
                e, EmptyVarException
            ), "Debería de saltar EmptyVarException"

    def testPezInDB(self):
        vessel, ais = Filter_Route(pez=self.p.Nombre_Comercial)

        assert len(ais) != 0, "No debería de estar vacío"
        assert len(vessel) != 0, "No debería de estar vacío"

    def testPezNotInDB(self):
        vessel, ais = Filter_Route(pez="Pez random")

        assert len(ais) == 0, "Debería de estar vacío"
        assert len(vessel) == 0, "Debería de estar vacío"

    def testOutputFull(self):
        vessel, ais = Filter_Route()
        assert len(ais) == 2, "No debería de estar vacío"
        assert len(vessel) == 1, "No debería de estar vacío"
