from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("2/", views.index2, name="index2"),
    path("maproute/", views.maproute, name="maproute"),
    path("maproutelayer/", views.maproutelayer, name="maproutelayer"),
    path("maproutefilter/", views.maproutefilter, name="maproutefilter"),
    path("search/", views.search, name="search"),
    path("plot/", views.plotpage, name="plot"),
]
