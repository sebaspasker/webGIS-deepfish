from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from flask import json
from .forms import SearchForm, SearchIndexForm
import urllib.request
from webgisapp.models import AISVessel, Vessel
from webgisapp.utils.filter import Filter_Route, Filter_Type, filterDictForm
from webgisapp.utils.plot_data_kg_travel import PlotController
from webgisapp.utils.join_travel import Join_Travels, Comprobe_Possible_Join_Travels
from webgisapp.utils.polygon_geojson import polygon_mile_geojson, search_min_max_ais


# Mapa de calor
def index(request):
    if request.method == "POST":
        form = SearchIndexForm()
        dict_form = {}
        for i in range(1, 7):
            dict_form["option_" + str(i)] = request.POST.get("select_" + str(i))
            dict_form["text_input_" + str(i)] = request.POST.get("text_input_" + str(i))
        mmsi, date_from, date_to, talla, especie, posicion = filterDictForm(dict_form)
        v, ais = Filter_Route(mmsi, date_from, date_to, talla, especie, posicion)
        if Comprobe_Possible_Join_Travels(ais, vessels=v):
            Join_Travels(vessels=v, aiss=ais)
        # Elegimos en base al tipo
        collection, route, typee = Filter_Type("Heat", v, ais)
        return render(
            request,
            route,
            {
                "form": form,
                "MMSI": "123",
                "VesselName": "El Buque",
                "LON": 12.65,
                "LAT": 12.43,
                "COG": "1.0",
                "SOG": "3.0",
                "BaseDateTime": str(datetime.now()),
                "CallSign": "321",
                "VesselType": "A",
                "Length": "5m",
                "Width": "2m",
                "Cargo": "A",
                "TransceiverClass": "A",
                "collection": collection,
                "type": typee,
            },
        )
    else:
        collection, route, typee = Filter_Type(
            "Heat", Vessel.objects.all(), AISVessel.objects.all()
        )
        return render(
            request,
            route,
            {
                "collection": collection,
                "type": typee,
                "form": form,
                "MMSI": "123",
                "VesselName": "El Buque",
                "LON": 12.65,
                "LAT": 12.43,
                "COG": "1.0",
                "SOG": "3.0",
                "BaseDateTime": str(datetime.now()),
                "CallSign": "321",
                "VesselType": "A",
                "Length": "5m",
                "Width": "2m",
                "Cargo": "A",
                "TransceiverClass": "A",
            },
        )


# Mapa de calor
def index2(request):
    if request.method == "POST":
        form = SearchIndexForm()
        dict_form = {}
        for i in range(1, 7):
            dict_form["option_" + str(i)] = request.POST.get("select_" + str(i))
            dict_form["text_input_" + str(i)] = request.POST.get("text_input_" + str(i))
        mmsi, date_from, date_to, talla, especie, posicion = filterDictForm(dict_form)
        v, ais = Filter_Route(mmsi, date_from, date_to, talla, especie, posicion)

        collection, route, typee = Filter_Type("PointAndLine", v, ais)

        collection_individual, _, _ = Filter_Type("Heat", v, ais)

        if Comprobe_Possible_Join_Travels(ais, vessels=v):
            Join_Travels(vessels=v, aiss=ais)
        return render(
            request,
            "webgisapp/map/map_index2.html",
            {
                "MMSI": "123",
                "VesselName": "El Buque",
                "LON": 12.65,
                "LAT": 12.43,
                "COG": "1.0",
                "SOG": "3.0",
                "BaseDateTime": str(datetime.now()),
                "CallSign": "321",
                "VesselType": "A",
                "Length": "5m",
                "Width": "2m",
                "Cargo": "A",
                "TransceiverClass": "A",
                "collection": collection,
                "collection_individual": collection_individual,
                "type": typee,
                "form": SearchIndexForm(),
            },
        )
    else:
        form = SearchIndexForm()
        collection, route, typee = Filter_Type(
            "PointAndLine", Vessel.objects.all(), AISVessel.objects.all()
        )
        collection_individual, _, _ = Filter_Type(
            "Heat", Vessel.objects.all(), AISVessel.objects.all()
        )

        return render(
            request,
            "webgisapp/map/map_index2.html",
            {
                "MMSI": "123",
                "VesselName": "El Buque",
                "LON": 12.65,
                "LAT": 12.43,
                "COG": "1.0",
                "SOG": "3.0",
                "BaseDateTime": str(datetime.now()),
                "CallSign": "321",
                "VesselType": "A",
                "Length": "5m",
                "Width": "2m",
                "Cargo": "A",
                "TransceiverClass": "A",
                "collection": collection,
                "collection_individual": collection_individual,
                "type": typee,
                "form": SearchIndexForm(),
            },
        )


def index3(request):
    start_tuple, end_tuple = search_min_max_ais()
    print(start_tuple, end_tuple)
    return render(
        request,
        "webgisapp/map/map_index3.html",
        {
            "collection": polygon_mile_geojson(
                start_tuple,
                end_tuple
                # (-0.45332507935470845, 38.338489735664446),
                # (-0.39798242386968524, 38.3145996069299),
            ),
        },
    )


import requests


def plotpage(request, option):
    input_option = 4
    if option == 1:
        input_option = 1
    elif option == 2:
        input_option = 4
    elif option == 3:
        input_option = 5
    data_keys, data_values, y = PlotController(
        input_option,
        # datetime.now() - timedelta(days=1),
        # datetime.now() + timedelta(days=5),
    )

    source = requests.get(
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Alicante/today?unitGroup=metric&elements=temp%2Cwindspeed&include=current&key=WNLS765U59WBFAWKRW3GCAVAW&contentType=json"
    ).text

    list_of_data = json.loads(source)

    temperature = str(int(list_of_data["currentConditions"]["temp"]))
    windspeed = str(int(list_of_data["currentConditions"]["windspeed"]))

    return render(
        request,
        "webgisapp/map/map_plot.html",
        {
            "labels": [x.strftime("%Y-%m-%d") for x in list(data_keys)],
            "data": json.dumps(list(data_values)),
            "y": y,
            "temperature": temperature,
            "wind": windspeed,
        },
    )


# Mapa de rutas de tres rutas mmsi ejemplmv
def maproute(request):
    start_tuple, end_tuple = search_min_max_ais()
    print(start_tuple, end_tuple)
    return render(
        request,
        "webgisapp/maproute.html",
        {
            "collection": polygon_mile_geojson(
                start_tuple,
                end_tuple
                # (-0.45332507935470845, 38.338489735664446),
                # (-0.39798242386968524, 38.3145996069299),
            ),
        },
    )


# Mapa de rutas con filtrado y popups
def maproutelayer(request):
    return render(request, "webgisapp/maproute_layer.html")


# Búsqueda de rutas en base al MMSI
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # Recogemos información del form
            mmsi = form.cleaned_data["MMSI"]
            date_from = form.cleaned_data["init_date"]
            date_to = form.cleaned_data["end_date"]
            talla = form.cleaned_data["talla"]
            pez = form.cleaned_data["pez"]
            option = form.cleaned_data["option"]
            try:
                Type = ["Line", "Point", "PointAndLine", "Heat"][option]
                # Hacemos busquedad
                v, ais = Filter_Route(mmsi, date_from, date_to, talla, pez)
                if Comprobe_Possible_Join_Travels(ais, vessels=v):
                    Join_Travels(vessels=v, aiss=ais)
                # Elegimos en base al tipo
                collection, route, typee = Filter_Type(Type, v, ais)
                return render(request, route, {"collection": collection, "type": typee})
            except Exception as e:
                raise e
        else:
            # TODO poner error
            pass
    else:
        form = SearchForm()
        return render(request, "webgisapp/form.html", {"form": form})


# def plotpage(request):
#     # Vemos los datos que queremos representar y
#     # lo escribimos en plot.html
#     PlotController(
#         5, datetime.now() - timedelta(days=4), datetime.now() + timedelta(days=5)
#     )
#     return render(request, "webgisapp/plot_page.html")


def maproutefilter(request):
    return render(request, "webgisapp/maproute_filter.html")
