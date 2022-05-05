from datetime import datetime, timedelta
import random
from webgisapp.models import Fish, Plate, Fish_Plate
from django.core.management import BaseCommand
from webgisapp.management.commands.random_ais_generator import randomString

class Command(BaseCommand):
    help = "Random plate generator by existing fishes and existing vessels"
    
    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help="Number of random fish analysis")

    def handle(self, *args, **options):
        all_f = Fish.objects.all()
        all_p = Plate.objects.all()
        for i in range(0, options['n']):
            f = all_f[random.randrange(0, len(all_f))]
            p = all_p[random.randrange(0, len(all_p))]
            f_plate = Fish_Plate(Lote=p,
                                 Nombre_Cientifico=f,
                                 Talla_cm=random.randrange(0, 50),
                                 Cantidad=random.randrange(0,20),
                                 Peso=random.randrange(0,10))
            f_plate.save()
