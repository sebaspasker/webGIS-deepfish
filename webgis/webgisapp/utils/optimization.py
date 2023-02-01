import datetime
from webgisapp.models import *
from webgisapp.utils.filter import Filter_Type

"""
Optimization file with static off sync memory control
"""


def dump_db_to_geojson():
    (
        collection,
        _,
        _,
    ) = Filter_Type("Heat", Vessel.objects.all(), AISVessel.objects.all())
