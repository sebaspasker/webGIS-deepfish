from csv import DictReader
from django.core.management import BaseCommand
from datetime import datetime

from webgisapp.models import AISVessel
from webgisapp.models import Vessel

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class Command(BaseCommand):
    help = "Loads data from data.csv"

    def handle(self, *args, **options):
        for row in DictReader(open("./data.csv")):
            vessel=Vessel(MMSI=row['MMSI'], VesselName=row['VesselName'])
            vessel.save()
            da = row['BaseDateTime']
            da_int = list(map(int, (da[0:4], da[5:7], da[8:10], da[11:13], da[14:16], da[17:19])))
            d = datetime(da_int[0], da_int[1], da_int[2], da_int[3], da_int[4], da_int[5])
            AIS=AISVessel(MMSI=vessel,
                          BaseDateTime=d,
                          LAT=row['LAT'],
                          LON=row['LON'],
                          SOG=row['SOG'],
                          COG=row['COG'],
                          VesselName=row['VesselName'],
                          CallSign=row['CallSign'],
                          VesselType=row['VesselType'],
                          Status=row['Status'],
                          Length=row['Length'],
                          Width=row['Width'],
                          Cargo=row['Cargo'],
                          TransceiverClass=row['TransceiverClass'],
                         )
            AIS.save()
