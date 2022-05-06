from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from .forms import SearchForm
from geojson import FeatureCollection
from webgisapp.models import AISVessel, Vessel
from webgisapp.utils.ais_to_geojson import AISQuery_To_LineStringCollection


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
            mmsi = form.cleaned_data['MMSI']
            try:
                v = Vessel.objects.filter(MMSI__contains=mmsi)
                ais = AISVessel.objects.filter(MMSI__in=v)
                collection = AISQuery_To_LineStringCollection(v, ais)
                return render(request, 'webgisapp/maproute_search.html', {'collection' : collection})
            except Exception as e:
                raise e
    else:
        form = SearchForm()
        return render(request, 'webgisapp/form.html', {'form' : form})

# Búsqueda del MMSI pero desde el frontend (no busca en la base de datos) 
def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
