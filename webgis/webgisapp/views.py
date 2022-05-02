from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader


def index(request):
    return render(request, 'webgisapp/index.html')

def maproute(request):
    return render(request, 'webgisapp/maproute.html')
    
def maproutelayer(request):
    return render(request, 'webgisapp/maproute_layer.html')

