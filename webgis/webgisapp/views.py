from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader


def index(request):
    return render(request, 'webgisapp/index.html')

