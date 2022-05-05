from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.template import loader
from webgisapp.models import AISVessel, Vessel
from django.db.models import Q
from .forms import SearchForm


def index(request):
    return render(request, 'webgisapp/index.html')

def maproute(request):
    return render(request, 'webgisapp/maproute.html')
    
def maproutelayer(request):
    return render(request, 'webgisapp/maproute_layer.html')

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            mmsi = form.cleaned_data['MMSI']
            try:
                v = Vessel.objects.get(MMSI__contains=mmsi)
                ais = AISVessel.objects.filter(MMSI=v)
                return HttpResponse("<h4> Encontrado " + ais[0].to_string() + ais[1].to_string() +  "</h4>") 
            except Exception as e:
                raise e
    else:
        form = SearchForm()
        return render(request, 'webgisapp/form.html', {'form' : form})

def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
