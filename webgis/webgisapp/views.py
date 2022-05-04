from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from webgisapp.models import AISVessel, Vessel
from django.db.models import Q


def index(request):
    return render(request, 'webgisapp/index.html')

def maproute(request):
    return render(request, 'webgisapp/maproute.html')
    
def maproutelayer(request):
    return render(request, 'webgisapp/maproute_layer.html')

### TODO
def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        try:
            vessel = Vessel.objects.filter(VesselName__contains=search_id)
            ais = AISVessel.objects.filter(MMSI = vessel.first())
            print(ais)
            return render(request, 'webgisapp/route_search.html', {'ais' : ais})
        except AISVessel.DoesNotExist:
            return HttpResponse("No such vessel")
    else:
        return render(request, 'webgisapp/form.html')

def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
