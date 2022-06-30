import json

plate_file = "data_cln.csv"
fish_plate_file = "Medidas_entrada_con_h_con_peso.csv"
path = "/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/webgis/data/"


plates = {}

with open(path + plate_file, "r") as f:
    x = True
    for line in f:
        if x:
            x = False
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
            continue

        if line_split[0] not in plates:
            plates[line_split[0]] = {
                "lote": line_split[1],
                "matricula": matricula,
                "nombre": name,
                "puerto": "Campello",
                "zona captura": line_split[11][: len(line_split[11]) - 1],
                "fecha": line_split[6],
                "pez comercial": line_split[4],
                "pez cientifico": line_split[5],
                "kg bandeja": line_split[7],
                "armador": line_split[8],
                "tipo de pesca": line_split[9],
                "presentacion": line_split[10],
                "analisis": [],
            }

only_child = []
with open(path + fish_plate_file, "r") as f:
    for line in f:
        line_split = line.split(",")
        route = line_split[0]
        route = route[: route.index("B")] + "E" + route[route.index("B") + 1 :]

        bandeja = {
            "size": float(line_split[1]),
            "bbox1": line_split[2][1:],
            "bbox2": line_split[3],
            "bbox3": line_split[4],
            "bbox4": line_split[5][: len(line_split[5]) - 1],
            "specie": line_split[6],
            "grams": float(line_split[7][: len(line_split[7]) - 1]),
        }

        if route in plates:
            plates[route]["analisis"].append(bandeja)
        else:
            only_child.append(bandeja)


plates["only_child"] = {}
plates["only_child"]["analisis"] = only_child
with open(path + "data_plates.json", "w") as f:
    json.dump(plates, f)
