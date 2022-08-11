import random
import string
from datetime import datetime
from django.core.management import BaseCommand
from random import randrange
from webgisapp.models import *

fishes = {
    "Dentex dentex": "Dentón común",
    "Diplodus annularis": "Raspallón",
    "Diplodus sargus": "Sargo común",
    "Mullus surmuletus": "Salmonete de roca",
    "Mullus barbatus": "Salmonete de fango",
    "Merluccius merluccius": "Pescadilla",
    "Pagellus acarne": "Aligote",
    "Pagellus erythrinus": "Breca",
    "Pagrus pagrus": "Pargo",
    "Sarda sarda": "Bonito común",
    "Scorpaena porcus": "Pez escorpión negro",
    "Symphodus tinca": "Tordo",
    "Sphyraena sphyraena": "Barracuda",
    "Spicara maena": "Chucla",
    "Serranus scriba": "Serrano",
    "Seriola dumerili": "Pez limón",
    "Sparus aurata": "Dorada",
    "Sepia officinalis": "Sepia común",
}


class Command(BaseCommand):
    help = "Import Deepfish plates data"

    def handle(self, *args, **options):
        plate_file = "./data/data_cln.csv"
        fish_plate_file = "./data/Medidas_entrada_con_h_con_peso.csv"
        # import fishes
        for key in fishes.keys():
            f = Fish(Nombre_Cientifico=key, Nombre_Comercial=fishes[key])
            try:
                f.save()
            except Exception:
                continue

        path_plate = {}
        with open(plate_file, "r") as f:
            first = True
            for line in f:
                if first is True:
                    first = False
                    continue
                line_split = line.split(",")

                # Split name and matricula
                name_and_matricula = line_split[2].split(" ")
                name = ""
                for i in range(0, len(name_and_matricula)):
                    name += name_and_matricula[i]
                    if name_and_matricula[i] == "":
                        break
                    else:
                        name += " "
                if name_and_matricula[len(name_and_matricula) - 1] != "":
                    matricula = name_and_matricula[len(name_and_matricula) - 1]
                else:
                    matricula = name_and_matricula[len(name_and_matricula) - 2]
                if matricula == "" and name == "":
                    pass

                # Save Vessel

                vessels = Vessel.objects.all()
                v = vessels[randrange(0, len(vessels))]

                # v = Vessel(
                #     MMSI="".join(
                #         random.SystemRandom().choice(
                #             string.ascii_letters + string.digits
                #         )
                #         for _ in range(9)
                #     ).upper(),
                #     VesselName=name,
                #     Matricula=matricula,
                #     Image=None,
                # )

                # try:
                #     v.save()
                # except Exception:
                #     pass

                # Save Plate

                aiss = AISVessel.objects.filter(MMSI=v)
                random_ais = aiss[randrange(0, len(aiss))]

                # date = list(map(int, line_split[6].split("/")))  # Save date
                p = Plate(
                    Lote=line_split[1],
                    Matricula=v,
                    Puerto="Campello",
                    Zona_Captura=line_split[11][len(line_split[11]) - 1],
                    # Fecha_Inicio=datetime(date[0], date[1], date[2], 0, 0, 0),
                    # Fecha_Fin=datetime(date[0], date[1], date[2], 23, 59, 59),
                    Fecha_Inicio=datetime(
                        random_ais.BaseDateTime.year,
                        random_ais.BaseDateTime.month,
                        random_ais.BaseDateTime.day,
                        0,
                        0,
                        0,
                    ),
                    Fecha_Fin=datetime(
                        random_ais.BaseDateTime.year,
                        random_ais.BaseDateTime.month,
                        random_ais.BaseDateTime.day,
                        23,
                        59,
                        59,
                    ),
                    Nombre_Pez_Bandeja=line_split[5],
                    Kg_Bandeja=int(line_split[7][: len(line_split[7]) - 3]),
                )

                try:
                    p.save()
                except Exception:
                    print("Plate EXIST ALREADY:")

                route = line_split[0]
                route = route[: route.index("E")] + "B" + route[route.index("E") + 1 :]
                path_plate[route] = {
                    "matricula": p.Matricula,
                    "timestamp": p.Timestamp
                    # "Lote": p.Lote,
                    # "Puerto": p.Puerto,
                    # "Zona_Captura": p.Zona_Captura,
                    # "Fecha_Inicio": p.Fecha_Inicio,
                    # "Fecha_Fin": p.Fecha_Fin,
                    # "Nombre_Pez_Bandeja": p.Nombre_Pez_Bandeja,
                    # "Kg": p.Kg_Bandeja,
                }

        with open("./data/Medidas_entrada_con_h_con_peso.csv") as f:
            # plates = []
            for line in f:
                line_split = line.split(",")
                file = line_split[0]
                talla = line_split[1]
                specie = line_split[6]
                gramos = line_split[7]
                try:
                    dic = path_plate[file]
                except Exception:
                    continue

                dic = path_plate[file]

                # p = Plate(
                #     Lote=dic["Lote"],
                #     Matricula=dic["Matricula"],
                #     Puerto=dic["Puerto"],
                #     Zona_Captura=dic["Zona_Captura"],
                #     Fecha_Inicio=dic["Fecha_Inicio"],
                #     Fecha_Fin=dic["Fecha_Fin"],
                #     Nombre_Pez_Bandeja=dic["Nombre_Pez_Bandeja"],
                #     Kg_Bandeja=dic["Kg"],
                # )

                # try:
                #     if p not in plates:
                #         p.save()
                #         plates.push(p)
                # except Exception:
                #     continue

                f = Fish_Plate(
                    # Plate=p,
                    Plate=Plate.objects.filter(Timestamp=dic["timestamp"]).first(),
                    Nombre_Cientifico=Fish.objects.filter(
                        Nombre_Cientifico=specie
                    ).first(),
                    Talla_cm=float(talla),
                    Peso=float(gramos),
                )

                try:
                    f.save()
                except Exception as e:
                    pass
        for plate in Plate.objects.all():
            fish_plates = Fish_Plate.objects.filter(Plate=plate)
            if len(fish_plates) == 0:
                plate.delete()
