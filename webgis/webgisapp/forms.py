from django import forms

class SearchForm(forms.Form):
    MMSI = forms.CharField(label="MMSI", max_length=9)
    # Init_Date = forms.DateTimeField(label="Init date time")
    # End_Date = forms.DateTimeField(label="End date time")
    # Talla = forms.IntegerField(label="Talla")
    # Especie = forms.CharField(label="Pez", max_length=30)
