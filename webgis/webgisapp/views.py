from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from webgisapp.models import AISVessel


def index(request):
    return render(request, 'webgisapp/index.html')

def maproute(request):
    return render(request, 'webgisapp/maproute.html')
    
def maproutelayer(request):
    return render(request, 'webgisapp/maproute_layer.html')

def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('textfield', None)
        try:
            Vessel = AISVessel.objects.get(VesselName = search_id)
            html = ("<H1>%s<H1>", Vessel.to_string())
            return HttpResponse(html)
        except AISVessel.DoesNotExist:
            return HttpResponse("No such vessel")
    else:
        return render(request, 'webgisapp/form.html')

def maproutefilter(request):
    return render(request, 'webgisapp/maproute_filter.html')
