import datetime
import random
import string
import names
from django.core.management import BaseCommand
from webgisapp.models import Vessel, AISVessel

def randomString(n):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits).upper() for _ in range(n))
 
class Command(BaseCommand):
    help = "Create random AIS related to random existing vessels"

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help="Number of ais")
        parser.add_argument('MAX_LAT', type=float, help="Max Latitude")
        parser.add_argument('MIN_LON', type=float, help="Min Latitude")
        parser.add_argument('MIN_LAT', type=float, help="Max Longitude")
        parser.add_argument('MAX_LON', type=float, help="Min Longitude")

    def handle(self, *args, **options):
        all_v = Vessel.objects.all()
        for i in range(0, options['n']):
            LAT = random.uniform(options['MIN_LAT'], options['MAX_LAT'])
            LON = random.uniform(options['MIN_LON'], options['MAX_LON'])
            v = all_v[random.randrange(0, len(all_v))]
            ais = AISVessel(MMSI=v,
                            BaseDateTime=datetime.datetime.now(),
                            LAT=LAT,
                            LON=LON,
                            SOG=random.randrange(0,10),
                            COG=random.randrange(0,10),
                            VesselName=v.VesselName,
                            CallSign=randomString(6),
                            VesselType=random.randrange(0,10),
                            Status=random.randrange(0,10),
                            Length=random.randrange(0,10),
                            Width=random.randrange(0,10),
                            Cargo=random.randrange(0,10),
                            TransceiverClass=random.choices(string.ascii_uppercase, k=1)
                           )
            ais.save()
