from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('maproute/', views.maproute, name='maproute'),
    path('maproutelayer/', views.maproutelayer, name='maproutelayer'),
    path('search/', views.search, name='search')
]
