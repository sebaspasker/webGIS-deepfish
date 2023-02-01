import pandas as pd
import random
import names

path="/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/project/csv/"
file_name="random_selective_AIS_Alicante.csv"

# MAX_LAT=38.437177
# MIN_LON=-0.306002
# MIN_LAT=37.688099
# MAX_LON=0.422470

MAX_LAT=38.399842489107726
MIN_LON=-0.32832330520082365
MIN_LAT=38.35218534919604
MAX_LON=-0.2760946070636072
38.35218534919604, -0.2760946070636072

LAT_L=[random.uniform(MIN_LAT, MAX_LAT) for x in range(100)]
LON_L=[random.uniform(MIN_LON, MAX_LON) for x in range(100)]
NAMES_L=[names.get_first_name() for x in range(100)]

csv_dict={'MMSI': [367773370 for x in range(100)],
          'BaseDateTime' : ["2018-01-01T08:01:11" for x in range(100)],
          'LAT' : LAT_L,
          'LON' : LON_L,
          'SOG' : [0.2 for x in range(100)],
          'COG' : [322.5 for x in range(100)],
          'VesselName' : NAMES_L,
          'CallSign' : ['WDJ3994' for x in range(100)],
          'VesselType' : [31 for x in range(100)],
          'Status' : [0 for x in range(100)],
          'Length' : [21 for x in range(100)],
          'Width' : [7 for x in range(100)],
          'Cargo' : [0 for x in range(100)],
          'TransceiverClass' : ['A' for x in range(100)]}

dataFrame = pd.DataFrame(csv_dict)
print("Dataframe...\n", dataFrame)

dataFrame.to_csv(path + file_name)
print("The output csv file written successfully and generated...")
