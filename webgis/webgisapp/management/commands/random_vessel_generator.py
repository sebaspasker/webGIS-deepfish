import random
import string
import names
from django.core.management import BaseCommand
from webgisapp.models import Vessel

class Command(BaseCommand):
    help = "Create random vessels"

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of vessels')

    def handle(self, *args, **options):
        for i in range(0, options['n']):
            mmsi = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(9))
            name = names.get_first_name()
            matricula = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
            v = Vessel(MMSI=mmsi.upper(), VesselName=name, Matricula=matricula.upper())
            v.save()

 
