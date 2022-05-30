from calendar import c
from queue import Empty
from time import time

from numpy import true_divide
import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupPlotController
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.plot_data_kg_travel import PlotController

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestPlotController:
    pytestmark = pytest.mark.django_db

    def setup(self): 
        setupPlotController(self) 

    def testWrongOptionValue(self):
        opt = "a"
        # Solo nos interesa lanzar la excepcion de option
        # No necesitamos crear dates correctas
        try:
            PlotController(
                option=opt, date_init=datetime.now(), date_end=datetime.now()
            )
        except Exception as e:
            assert isinstance(
                e, IncorrectOptionException
            ), "Debería de saltar IncorrectOptionException"


    def testMissingOption(self):
        try:
            PlotController(
                date_init=datetime.now(), date_end=datetime.now()
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"

    
    def testNoDate(self):
        try:
            PlotController(
                option=1
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"

    def testMissingInitDate(self):
        date_from   = datetime.now() - timedelta(days=5),

        try:
            PlotController(
                option=1, date_init=date_from
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"

    def testMissingEndDate(self):
        date_to   = datetime.now() - timedelta(days=5),

        try:
            PlotController(
                option=1, date_end=date_to
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"




    def testDateNotInDB(self):
        # Ponemos la fecha incorrecta para que salte error
        # date_init y date_end tienen los valores cambiados para lanzar la excepcion
        date_from   = datetime.now() - timedelta(days=5),
        date_to     = datetime.now() - timedelta(days=2),

        try:
            PlotController(
                option=1, date_init=date_to, date_end=date_from
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"



    def testAISEqualsNone(self):
        noAIS = None
        try:
            PlotController(
                option=2, date_init=datetime.now(), date_end=datetime.now(), ais=noAIS
            )
        except Exception as e:
            assert isinstance(
                e, EmptyVarException
            ), "Debería de saltar EmptyVarException"
    





