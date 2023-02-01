from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime


class SearchForm(forms.Form):
    MMSI = forms.CharField(label="MMSI", max_length=9, required=False)
    init_date = forms.DateField(
        label="Inicio", widget=AdminDateWidget(), required=False
    )
    end_date = forms.DateField(label="Fin", widget=AdminDateWidget(), required=False)
    talla = forms.IntegerField(label="Talla", required=False)
    pez = forms.CharField(label="Pez", max_length=30, required=False)
    option = forms.IntegerField(label="Opción", required=True)


class SearchIndexForm(forms.Form):
    colors = (
        ("mmsi", "MMSI"),
        ("fecha_inicio", "Fecha inicio"),
        ("fecha_fin", "Fecha fin"),
        ("talla", "Talla"),
        ("especie", "Especie"),
        ("posicion", "Posicion"),
    )

    select_1 = forms.ChoiceField(choices=colors)
    text_input_1 = forms.CharField(label="Input", max_length=20, required=True)
    select_2 = forms.ChoiceField(choices=colors)
    text_input_2 = forms.CharField(label="Input", max_length=20, required=True)
    select_3 = forms.ChoiceField(choices=colors)
    text_input_3 = forms.CharField(label="Input", max_length=20, required=True)
    select_4 = forms.ChoiceField(choices=colors)
    text_input_4 = forms.CharField(label="Input", max_length=20, required=True)
    select_5 = forms.ChoiceField(choices=colors)
    text_input_5 = forms.CharField(label="Input", max_length=20, required=True)
    select_6 = forms.ChoiceField(choices=colors)
    text_input_6 = forms.CharField(label="Input", max_length=20, required=True)


# options = (
# )
# select = forms.ChoiceField(choices=options)
