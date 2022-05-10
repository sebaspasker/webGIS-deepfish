from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from .forms import SearchForm
from geojson import FeatureCollection
from webgisapp.models import AISVessel, Vessel
from webgisapp.utils.ais_to_geojson import AISQuery_To_LineStringCollection
from webgisapp.utils.filter import Filter_Route


# Mapa de calor 
def index(request):
    return render(request, 'webgisapp/index.html')

# Mapa de rutas de tres rutas mmsi ejemplo
def maproute(request):
    return render(request, 'webgisapp/maproute.html')
    
# Mapa de rutas con filtrado y popups
def maproutelayer(request):
    return render(request, 'webgisapp/maproute_layer.html')

# Búsqueda de rutas en base al MMSI
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Recogemos información del form
            mmsi = form.cleaned_data['MMSI']
            date_from = form.cleaned_data['init_date']
            date_to = form.cleaned_data['end_date']
            talla = form.cleaned_data['talla']
            pez = form.cleaned_data['pez']
            try:
                # Hacemos busquedad
                v, ais = Filter_Route(mmsi, date_from, date_to, talla, pez)
                # Pasamos a GEOJson
                collection = AISQuery_To_LineStringCollection(v, ais)
                return render(request, 'webgisapp/maproute_search.html', {'collection' : collection})
            except Exception as e:
                raise e
        else:
            # TOOD poner error
            pass
    else:
        form = SearchForm()
        return render(request, 'webgisapp/form.html', {'form' : form})


def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
