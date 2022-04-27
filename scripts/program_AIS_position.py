# https://plotly.com/python/mapbox-layers/

token = "pk.eyJ1IjoiZXNzZWRlcGUiLCJhIjoiY2wxbmVrcGtpMDl2bTNrbzF3ajYxdzc2biJ9.vPfgY7bUBFnO2-NCJ96IEA"
import pandas as pd
vessels = pd.read_csv("/home/sebas_pasker/Documents/Trabajo_Investigacion/Deepfish2/cuadro_mando/project/webGIS/project/csv/random_selective_ALL_Alicante.csv")


import plotly.express as px

fig = px.scatter_mapbox(vessels, lat="LAT", lon="LON", hover_name="VesselName", hover_data=["VesselType", "TransceiverClass"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
