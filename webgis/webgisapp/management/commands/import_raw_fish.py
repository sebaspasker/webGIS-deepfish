from django.core.management import BaseCommand
from datetime import datetime

from webgisapp.models import Fish

class Command(BaseCommand):
    help = "Loads fish data from a txt raw file"
    
    def handle(self, *args, **options):
        try:
            file = open("data/fishes_clean.txt", 'r')
            first_attribute = True
            for line in file.readlines():
                if first_attribute:
                    comercial = line
                    first_attribute = False
                else:
                    cientifico = line
                    fish = Fish(Nombre_Cientifico=cientifico, 
                                Nombre_Comercial=comercial)
                    fish.save()
                    first_attribute = True
            file.close()
        except Exception as e:
            print("Ha habido un error: {}".format(e))
