from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound
from .forms import SearchForm
from webgisapp.models import AISVessel, Vessel
from webgisapp.utils.filter import Filter_Route, Filter_Type
from webgisapp.utils.plot_data_kg_travel import PlotController


# Mapa de calor 
def index(request):
    return render(request, 'webgisapp/index.html')

# Mapa de rutas de tres rutas mmsi ejemplmv
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
            option = form.cleaned_data['option']
            try:
                Type = ['Line', 'Point', 'PointAndLine', 'Heat'][option]
                # Hacemos busquedad
                v, ais = Filter_Route(mmsi, date_from, date_to, talla, pez)
                # Elegimos en base al tipo
                collection, route, typee = Filter_Type(Type, v, ais)
                return render(request, route, {'collection' : collection, 'type':typee})
            except Exception as e:
                raise e
        else:
            # TODO poner error
            pass
    else:
        form = SearchForm()
        return render(request, 'webgisapp/form.html', {'form' : form})


def plotpage(request):
    # Vemos los datos que queremos representar y
    # lo escribimos en plot.html
    PlotController(5, datetime.now() - timedelta(days=4), datetime.now() + timedelta(days=5))
    return render(request, 'webgisapp/plot_page.html')

def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
