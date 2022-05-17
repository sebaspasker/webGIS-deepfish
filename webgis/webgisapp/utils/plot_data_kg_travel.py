import numpy as np
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from webgisapp.models import AISVessel, Travel, Plate, Vessel, Fish_Plate, Fish
from datetime import datetime

class IncorrectOptionException(Exception):
    "Exception for incorrect option introduction"
    def __init__(self, message="Option invalid"):
        super().__init__(self.message)

class EmptyVarException(Exception):
    "Exception for an empty variable"
    def __init__(self, message="Empty value"):
        super().__init__(self,message)

    

def TimeKgAIS(ais_v, date_init, date_end, specie=False, specie_name="", amount=False):
    """
    Gets AIS, init date, end date, optionally specie and vessel amount boolean and returns 
    the kgs of fish or the amount of vessels based on date.
    """
    data = {}
    for day in pd.date_range(date_init, date_end, freq='D'):
        kgs = 0
        # Search AIS in marked day
        aiss = AISVessel.objects.filter(BaseDateTime__gt=day.replace(hour=00, minute=00, second=0),
                                            BaseDateTime__lt=day.replace(hour=23, minute=59, second=59))
        if not amount:
            for ais in aiss:
                    # Search fish plates
                    travels = Travel.objects.filter(AIS_fk=ais)

                    if specie:
                        if ''.__eq__(specie_name): # In case empty specie name and var True
                            raise  EmptyVarException
                        # Search fish plates based on fish specie
                        fishes = Fish.objects.filter(Nombre_Cientifico__startswith=specie_name)
                        fish_plates = Fish_Plate.objects.filter(Nombre_Cientifico__in=fishes)
                    else:
                        fish_plates = Fish_Plate.objects.all()
                    # Search Weight
                    fish_plates_kg = fish_plates.filter(Lote__in=[travel.Plate_fk for travel in travels]) \
                                                    .values_list('Peso', flat=True)
                    for kg in fish_plates_kg:
                        kgs += kg
            data[day] = kgs
        else:
            # In case amount True save length of vessels array
            data[day] = len(set(aiss.all().values_list('MMSI', flat=True)))
    return data

def PlotController(option, date_init, date_end, ais=None, specie_name=''):
    if option == 1:
        # TODO
        # Time Kg All AIS
        data = TimeKgAIS(AISVessel.objects.all(), date_init, date_end)
        y = "AIS vessels"
    elif option == 2:
        # TODO
        # Time Kg Some AIS
        if ais is not None:
            data = TimeKgAIS(ais, date_init, date_end)
        else:
            raise EmptyVarException
        y = "AIS vessels"
    elif option == 3:
        # TODO 
        # Time Kg By Specie
        data = TimeKgAIS(ais, date_init, date_end, specie=True, specie_name=specie_name)
        y = "AIS vessels based on specie"
    elif option == 4:
        # TODO
        # Amount of vessel based on time
        data = TimeKgAIS(AISVessel.objects.all(), date_init, date_end, amount=True)
        y = "Number of vessels"
    else:
        raise IncorrectOptionException
    BarPlotData(data, "./webgisapp/templates/webgisapp/plot.html", xlabel="Date/Time", )



def BarPlotData(data, output_path, xlabel="", ylabel=""):
    """
    Conversion of data x/y structure to html bar plot template for web representation
    Input: 
        Data {}, output_path String, xlabel String="", ylabel String=""
    """
    barWidth = 0.25
    courses = data.keys()
    values = data.values()

    fig = plt.figure(figsize=(10,5))
    plt.bar(courses, values, color='red', width=0.4)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    html_str = mpld3.fig_to_html(fig)
    html_file = open(output_path, "w")
    html_file.write(html_str)
    html_file.close()
    

# representVesselKg({'1234542': 10.4, 'asadasas' : 4.5, 'asdsadsa': 7.0}, "../templates/webgisapp/plot.html")
# TimeKgAIS(AISVessel.objects.all(), datetime.now(), datetime.now())


