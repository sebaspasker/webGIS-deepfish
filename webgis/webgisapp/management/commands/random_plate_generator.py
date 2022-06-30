from datetime import datetime, timedelta
import random
from webgisapp.models import Fish, Plate, Vessel
from django.core.management import BaseCommand
from webgisapp.management.commands.random_ais_generator import randomString

ports = ["Campello", "Santa Pola", "Benidorm", "Torrevieja", "Alicante"]


class Command(BaseCommand):
    help = "Random plate generator by existing fishes and existing vessels"

    def add_arguments(self, parser):
        parser.add_argument("n", type=int, help="Number of random plates")
        parser.add_argument("d", type=int, help="Number of days")

    def handle(self, *args, **options):
        all_f = Fish.objects.all()
        all_v = Vessel.objects.all()
        for i in range(0, options["n"]):
            f = all_f[random.randrange(0, len(all_f))]
            v = all_v[random.randrange(0, len(all_v))]
            plate = Plate(
                Lote=randomString(6),
                Matricula=v,
                Puerto=ports[random.randrange(0, len(ports))],
                Zona_Captura=randomString(2),
                Fecha_Inicio=datetime.now() + timedelta(days=options["d"]),
                Fecha_Fin=datetime.now()
                + timedelta(hours=1)
                + timedelta(days=options["d"]),
                Nombre_Pez_Bandeja=f.Nombre_Comercial,
                Kg_Bandeja=random.randrange(1, 20),
            )
            plate.save()
