lines = {}
with open(
    "/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/webgis/data/data_cln.csv",
    "r",
) as file:
    for line in file:
        line_split = line.split(",")
        route = line_split[0]
        route = route[: route.index("E")] + "B" + route[route.index("E") + 1 :]
        lines[route] = line[: len(line) - 1] + "\n"

only_child = []

with open(
    "/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/webgis/data/Medidas_entrada_con_h_con_peso.csv",
    "r",
) as file:
    for line in file:
        line_split = line.split(",")
        route = line_split[0]
        if route in lines:
            lines[route] += line[: len(line) - 1] + "\n"
        else:
            only_child.append(line)

with open(
    "/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/webgis/data/data_join.csv",
    "w",
) as file:
    for key in lines.keys():
        file.write(lines[key] + "\n")

    file.write("\nBANDEJAS SIN QR\n")
    for line in only_child:
        file.write(line)
