from django.core.management import BaseCommand

import os

from webgisapp.models import Vessel


class Command(BaseCommand):
    help = "Select a image for each vessel in DB"

    def handle(self, *args, **options):
        imgs = os.listdir("webgisapp/static/img/ships")
        i = 0
        size = len(imgs)
        for vessel in Vessel.objects.all():
            vessel.Image = imgs[i % size]
            i += 1
            vessel.save()
