import cv2
from pyzbar.pyzbar import decode
import os
from tqdm import tqdm
import numpy as np

base_route = "/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/deepfish-webgis/data/imgs/Imágenes"

dirs = os.listdir(base_route)
w_file = open("data.csv", "w")


def qr_detection(cv_img, path):
    qr_data = decode(cv_img)
    # En caso de que no se detecte el QR se filtra con un treshold para poder eliminar ruido y sombras de la imagen
    if qr_data == []:
        # PASO 1: CAMBIAR DE ESPACIO DE COLOR A HSV Y USAR EL CANAL V
        hsv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV_FULL)
        hsv = cv2.split(hsv)
        img = hsv[2]

        # PASO 2: APLICAR VARIOS THRESHOLD HASTA ENCONTRAR EL QUE PERMITA LA DETECCION DEL QR
        for i in range(2, 6, 2):
            res1 = cv2.adaptiveThreshold(
                img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 301, i
            )
            res2 = cv2.morphologyEx(res1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

            qr_data = decode(res2)

            # PASO 3: SI SE HA DETECTADO EL QR, IMPRIMIR EL RESULTADO
            if qr_data != []:
                w_file.write(
                    path
                    + ","
                    + qr_data[0].data.decode("utf-8").replace("\r\n", ",")
                    + "\n"
                )

    # IMPRIMIR DATOS DEL QR DE LAS IMAGENES QUE NO HA SIDO NECESARIO FILTRAR
    else:
        w_file.write(
            path + "," + qr_data[0].data.decode("utf-8").replace("\r\n", ",") + "\n"
        )


for directory, j in zip(dirs, tqdm(range(len(dirs)))):
    files = list(
        filter(lambda x: x.startswith("E"), os.listdir(base_route + "/" + directory))
    )
    for file, i in zip(files, tqdm(range(len(files)))):
        img = cv2.imread(base_route + "/" + directory + "/" + file)
        qr_detection(img, directory + "/" + file)
