from datetime import datetime, timedelta
import random
from random import randrange
from webgisapp.models import AISVessel, Vessel
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "Random route generator of 2-10 ais connected to same vessel"

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help="Number of random 1-10 ais routes")
        parser.add_argument('MAX_LAT', type=float, help="Max Latitude")
        parser.add_argument('MIN_LON', type=float, help="Min Latitude")
        parser.add_argument('MIN_LAT', type=float, help="Max Longitude")
        parser.add_argument('MAX_LON', type=float, help="Min Longitude")
        parser.add_argument('DAYS', type=int, help="Days less/more than today")

    def handle(self, *args, **options):
        all_v = Vessel.objects.all()
        for i in range(0, options['n']):
            LAT = random.uniform(options['MIN_LAT'], options['MAX_LAT'])
            LON = random.uniform(options['MIN_LON'], options['MAX_LON'])
            diff_LAT = [-0.001, 0, 0.001][randrange(0,3)]
            diff_LON = [-0.001, 0, 0.001][randrange(0,3)]
            if diff_LAT == 0 and diff_LON == 0:
                diff_LON = [-0.001, 0.001][randrange(0,2)]
            v = all_v[random.randrange(0, len(all_v))]
            days_less_more = options['DAYS']
            if  days_less_more >= 0:
                time = datetime.now() + timedelta(days=days_less_more)
            else:
                time = datetime.now() - timedelta(days=days_less_more)
            for i in range(0, randrange(3, 11)):
                ais = AISVessel(MMSI=v,
                                BaseDateTime=time,
                                LAT=LAT,
                                LON=LON,
                                SOG=random.randrange(0,10),
                                COG=random.randrange(0,10),
                                VesselName=v.VesselName,
                                CallSign='A',
                                VesselType=random.randrange(0,10),
                                Status=random.randrange(0,10),
                                Length=random.randrange(0,10),
                                Width=random.randrange(0,10),
                                Cargo=random.randrange(0,10),
                                TransceiverClass='A'
                                )
                LAT = LAT + diff_LAT
                LON = LON + diff_LON
                time = time + timedelta(minutes=2)
                ais.save()
                print(ais)
