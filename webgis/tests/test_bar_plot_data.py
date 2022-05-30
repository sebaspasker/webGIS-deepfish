from calendar import c
from email import message
from queue import Empty
from re import template
from time import time

from numpy import true_divide
import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupBarPlotData
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.plot_data_kg_travel import BarPlotData

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestBarPlotData:
    pytestmark = pytest.mark.django_db

    def setup(self): 
        setupBarPlotData(self) 

    def testNoData(self):
        nodata = None
        try:
            BarPlotData(
                data=nodata, output_path = ""
            )
        except Exception as e:
            template = "An exception of type {0} occured. Arguments: \n{1!r}"
            message = template

            assert isinstance(
                e, Exception
            ), "Debería de saltar Exception"
    








