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
    date_init=None,
    date_end=None,
    specie=False,
    specie_name="",
    amount=False,
    amount_of_ais=False,
):
    """
    Gets AIS, init date, end date, optionally specie and vessel amount boolean and returns
    the kgs of fish or the amount of vessels based on date.
    """
    if ais_v is None:
        ais_v = AISVessel.objects.all()

    data = {}
    if date_init is not None and date_end is not None:
        for day in pd.date_range(date_init, date_end, freq="D"):
            kgs = 0
            # Search AIS in marked day
            aiss = ais_v.filter(
                BaseDateTime__gt=day.replace(hour=00, minute=00, second=0),
                BaseDateTime__lt=day.replace(hour=23, minute=59, second=59),
            )
            if not amount and not amount_of_ais:
                for ais in aiss:
                    # Search fish plates
                    travels = Travel.objects.filter(AIS_fk=ais)
                    if Comprobe_Outdated_Travels(travels):
                        Delete_None_Existing_Travels(travels)
                        Join_Travels(travels)

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
                        Plate__in=[travel.Plate_fk for travel in travels]
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
    else:
        days = []
        plates_used = []
        for ais in AISVessel.objects.all():
            dax = ais.BaseDateTime
            # day = datetime(dax.day, dax.month, dax.year)  # Incorrect save format
            day = datetime(dax.year, dax.month, dax.day)  # Incorrect save format
            kgs = 0
            travels = Travel.objects.filter(AIS_fk=ais).exclude(
                Plate_fk__in=plates_used,
            )
            plates_used += [travel.Plate_fk.Timestamp for travel in travels]

            if specie:
                if "".__eq__(
                    specie_name
                ):  # In case empty specie name and but boolean True
                    raise EmptyVarException
                # Search fish plates based on fish specie
                fishes = Fish.objects.filter(Nombre_Cientifico__startswith=specie_name)
                fish_plates = Fish_Plate.objects.filter(Nombre_Cientifico__in=fishes)
            else:
                fish_plates = Fish_Plate.objects.all()
            # Search Weight
            fish_plates_kg = fish_plates.filter(
                Plate__in=[travel.Plate_fk for travel in travels]
            ).values_list("Peso", flat=True)
            for kg in fish_plates_kg:
                kgs += kg

            if not amount and not amount_of_ais:
                if day not in data:
                    data[day] = 0
                    days.append(day)
                data[day] += kgs / 1000
            elif amount:
                # In case amount True save length of vessels array
                if day not in data:
                    data[day] = 0
                    days.append(day)
                data[day] += 1
            elif amount_of_ais:
                # In case amount_of_ais True save length of ais array
                if day not in data:
                    data[day] = 0
                    days.append(day)
                data[day] += 1
            else:
                print("EXCEPTION")
                raise Exception
    days.sort()
    data_s = {}
    for dayz in days:
        data_s[dayz] = data[dayz]
    return data_s.keys(), data_s.values()


def PlotController(option, date_init=None, date_end=None, ais=None, specie_name=""):
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
        data_keys, data_values = TimeKgAIS(AISVessel.objects.all(), date_init, date_end)
        y = "Kgs of fish"
    elif option == 2:
        # Time Kg Some AIS
        if ais is not None:
            data_keys, data_values = TimeKgAIS(ais, date_init, date_end)
        else:
            raise EmptyVarException
        y = "Kgs of fish"
    elif option == 3:
        # Time Kg By Specie
        data_keys, data_values = TimeKgAIS(
            ais, date_init, date_end, specie=True, specie_name=specie_name
        )
        y = "Kg of fish based on specie"
    elif option == 4:
        # Amount of vessel based on time
        data_keys, data_values = TimeKgAIS(
            AISVessel.objects.all(), date_init, date_end, amount=True
        )
        y = "Number of vessels"
    elif option == 5:
        # Amount of vessel based on time
        data_keys, data_values = TimeKgAIS(
            AISVessel.objects.all(), date_init, date_end, amount_of_ais=True
        )
        print(data_keys, data_values)
        y = "Number of AIS"
    else:
        raise IncorrectOptionException
    return data_keys, data_values, y


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
