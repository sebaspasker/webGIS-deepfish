from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

class SearchForm(forms.Form):
    MMSI = forms.CharField(label="MMSI", max_length=9, required=False)
    init_date = forms.DateField(label="Inicio", widget=AdminDateWidget(), required=False)
    end_date = forms.DateField(label="Fin", widget=AdminDateWidget(), required=False)
    talla = forms.IntegerField(label="Talla", required=False)
    pez = forms.CharField(label="Pez", max_length=30, required=False)
    option = forms.IntegerField(label="Opción", required=True)
