from datetime import datetime
from .exceptions import IncorrectOptionException, EmptyVarException
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from webgisapp.models import AISVessel, Travel, Plate, Vessel, Fish_Plate, Fish
from webgisapp.utils.join_travel import (
    Delete_None_Existing_Travels,
    Comprobe_Outdated_Travels,
)


def TimeKgAIS(
    ais_v,
    date_init,
    date_end,
    specie=False,
    specie_name="",
    amount=False,
    amount_of_ais=False,
):
    """
    Gets AIS, init date, end date, optionally specie and vessel amount boolean and returns
    the kgs of fish or the amount of vessels based on date.
    """
    data = {}
    for day in pd.date_range(date_init, date_end, freq="D"):
        kgs = 0
        # Search AIS in marked day
        aiss = AISVessel.objects.filter(
            BaseDateTime__gt=day.replace(hour=00, minute=00, second=0),
            BaseDateTime__lt=day.replace(hour=23, minute=59, second=59),
        )
        """
        if ais_v is None:
            aiss = AISVessel.objects.filter(
                BaseDateTime__gt=day.replace(hour=00, minute=00, second=0),
                BaseDateTime__lt=day.replace(hour=23, minute=59, second=59),
            )
        else:
            
            aiss = ais_v.filter(
                BaseDateTime__gt=day.replace(hour=00, minute=00, second=0),
                BaseDateTime__lt=day.replace(hour=23, minute=59, second=59),
            )
         
        """   
        if not amount and not amount_of_ais:
            for ais in aiss:
                # Search fish plates
                travels = Travel.objects.filter(AIS_fk=ais)
                if Comprobe_Outdated_Travels(travels):
                    Delete_None_Existing_Travels(travels)

                if specie:
                    if "".__eq__(
                        specie_name
                    ):  # In case empty specie name and but boolean True
                        raise EmptyVarException
                    # Search fish plates based on fish specie
                    fishes = Fish.objects.filter(
                        Nombre_Cientifico__startswith=specie_name
                    )
                    fish_plates = Fish_Plate.objects.filter(
                        Nombre_Cientifico__in=fishes
                    )
                else:
                    fish_plates = Fish_Plate.objects.all()
                # Search Weight
                fish_plates_kg = fish_plates.filter(
                    Lote__in=[travel.Plate_fk for travel in travels]
                ).values_list("Peso", flat=True)
                for kg in fish_plates_kg:
                    kgs += kg
            data[day] = kgs
        elif amount:
            # In case amount True save length of vessels array
            data[day] = len(set(aiss.all().values_list("MMSI", flat=True)))
        elif amount_of_ais:
            # In case amount_of_ais True save length of ais array
            data[day] = len(aiss)
        else:
            raise Exception
    return data


def PlotController(option, date_init, date_end, ais=None, specie_name=""):
    """
    Plot Controller: search based on ais data and plot it in html file.
    Options:
        1: All AIS based on a time range.
        2: Selective AIS based on a time range
        3: Selective AIS based on a specie in a time range
        4: Selective Vessels based on a time range
    """
    if option == 1:
        # Time Kg All AIS
        data = TimeKgAIS(AISVessel.objects.all(), date_init, date_end)
        y = "Kgs of fish"
    elif option == 2:
        # Time Kg Some AIS
        if ais is not None:
            data = TimeKgAIS(ais, date_init, date_end)
        else:
            raise EmptyVarException
        y = "Kgs of fish"
    elif option == 3:
        # Time Kg By Specie
        data = TimeKgAIS(ais, date_init, date_end, specie=True, specie_name=specie_name)
        y = "Kg of fish based on specie"
    elif option == 4:
        # Amount of vessel based on time
        data = TimeKgAIS(AISVessel.objects.all(), date_init, date_end, amount=True)
        y = "Number of vessels"
    elif option == 5:
        # Amount of vessel based on time
        data = TimeKgAIS(
            AISVessel.objects.all(), date_init, date_end, amount_of_ais=True
        )
        y = "Number of AIS"
    else:
        raise IncorrectOptionException
    print(data)
    BarPlotData(
        data, "./webgisapp/templates/webgisapp/plot.html", xlabel="Date/Time", ylabel=y
    )


def BarPlotData(data, output_path, xlabel="", ylabel=""):
    """
    Conversion of data x/y structure to html bar plot template for web representation
    Input:
        Data {}, output_path String, xlabel String="", ylabel String=""
    """
    barWidth = 0.25
    courses = data.keys()
    values = data.values()

    fig = plt.figure(figsize=(10, 5))
    plt.bar(courses, values, color="red", width=0.4)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    html_str = mpld3.fig_to_html(fig)
    html_file = open(output_path, "w")
    html_file.write(html_str)
    html_file.close()
















