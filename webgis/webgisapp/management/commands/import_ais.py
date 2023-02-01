import json
import random
from datetime import datetime
from django.core.management import BaseCommand
from tqdm import tqdm
from webgisapp.models import Vessel, AISVessel


class Command(BaseCommand):
    help = "Import ais data in json file"

    def handle(self, *args, **options):
        f = open("./data/ais_deepFish.json")
        data = json.load(f)
        for d, p1 in zip(data, tqdm(range(len(data.keys())))):
            v = Vessel(MMSI=d, Matricula=d, VesselName=d)
            try:
                v.save()
            except Exception:
                pass
            ais_t = [data[d][travel]["t"] for travel in data[d]]
            ais_lat = [data[d][travel]["lat"] for travel in data[d]]
            ais_lon = [data[d][travel]["lon"] for travel in data[d]]
            for travel, i, p2 in zip(
                data[d], range(len(data[d])), tqdm(range(len(data[d])))
            ):
                t_list = ais_t[i]
                lat_list = ais_lat[i]
                lon_list = ais_lon[i]
                for x in range(len(t_list)):
                    date = datetime.strptime(t_list[x], "%Y-%m-%d %H:%M:%S")
                    lat = lat_list[x]
                    lon = lon_list[x]
                    ais = AISVessel(
                        MMSI=v,
                        LAT=lat,
                        LON=lon,
                        BaseDateTime=date,
                        SOG=random.randrange(0, 10),
                        COG=random.randrange(0, 10),
                        VesselName=d,
                        CallSign="A",
                        VesselType=random.randrange(0, 10),
                        Status=random.randrange(0, 10),
                        Length=random.randrange(0, 10),
                        Width=random.randrange(0, 10),
                        Cargo=random.randrange(0, 10),
                        TransceiverClass="A",
                    )

                    try:
                        ais.save()
                    except Exception:
                        pass
