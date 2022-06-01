from calendar import c
from email import message
from queue import Empty
from re import template
from time import time

from numpy import datetime_as_string, true_divide
import pytest
from datetime import datetime, timedelta
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection
from .setups import setupTimeKgAIS
from webgisapp.utils.join_travel import *
from webgisapp.utils.abbr import *
from webgisapp.utils.exceptions import *
from webgisapp.utils.plot_data_kg_travel import *

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestTimeKgAIS:
    pytestmark = pytest.mark.django_db

    def setup(self): 
        setupTimeKgAIS(self)

    def testEmptyVarException(self):
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        try:
            TimeKgAIS(
                ais_v=aistest, date_init=dinit, date_end=dend, specie=True
            )
        except Exception as e:
            assert isinstance(
                e, EmptyVarException
            ), "Debería de saltar EmptyVarException"


    def testCorrectWeightWithSpecieName(self):
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        days         = pd.date_range(dinit, dend, freq="D")
        diccionario = TimeKgAIS(ais_v=aistest, date_init=dinit, date_end=dend, specie=True, specie_name="Pez1")
        # EN LA BBDD SOLO LA FISHPLATE 1 Y 2 TIENEN NOMBRECIENTIFICO = PEZ1
        # LA FISHPLATE 1 PESA 3 Y LA FISHPLATE 2 PESA 5
        assert diccionario[days[0]]==0
        assert diccionario[days[1]]==8


    def testCorrectWeightWithoutSpecieName(self):
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        days         = pd.date_range(dinit, dend, freq="D")
        diccionario = TimeKgAIS(ais_v=aistest, date_init=dinit, date_end=dend)
        # EN LA BBDD FISHPLATE1 PESA 3, FISHPLATE 2 PESA 5 Y FISHPLATE 3 PESA 15
        assert diccionario[days[0]]==0
        assert diccionario[days[1]]==23


    def testSpecieNameVarType(self):
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        aux         = 5
        try:
            TimeKgAIS(
                ais_v=aistest, date_init=dinit, date_end=dend, specie=True, specie_name=aux
            )
        except Exception as e:
            assert isinstance(
                # TODO NO ENTIENDO POR QUE SALTA EmptyVarException EN LUGAR DE TypeError 
                e, EmptyVarException
            ), "Debería de saltar EmptyVarException"


    def testWrongDate(self):
        # Ponemos la fecha incorrecta para que salte error
        # date_init y date_end tienen los valores cambiados para lanzar la excepcion
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now() - timedelta(days=5),
        dend        = datetime.now() - timedelta(days=2),

        try:
            TimeKgAIS(
                ais_v=aistest, date_init=dend, date_end=dinit
            )
        except Exception as e:
            assert isinstance(
                e, TypeError
            ), "Debería de saltar TypeError"


    def testAmountTrue(self):
        # TODO
        # COMPROBAR POR QUE EL ASSERT ES 1 CUANDO HAY 2 VESSEL QUE PASAN POR ESE AIS EL MISMO DIA
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        days         = pd.date_range(dinit, dend, freq="D")
        diccionario = TimeKgAIS(ais_v=aistest, date_init=dinit, date_end=dend, amount=True)
        assert diccionario[days[1]]==1


    def testAmountOfAISTrue(self):
        # COMPROBAMOS ANTEAYER Y AYER
        # NO HAY AIS CON FECHA -2 (ANTEAYER)
        # HAY AIS CON FECHA -1 (AYER)
        aistest     = AISVessel.objects.all()[0]
        dinit       = datetime.now()-timedelta(days=2)
        dend        = datetime.now()
        days         = pd.date_range(dinit, dend, freq="D")
        diccionario = TimeKgAIS(ais_v=aistest, date_init=dinit, date_end=dend, amount_of_ais=True)
        assert diccionario[days[0]]==0 
        assert diccionario[days[1]]==2 #AIS-1 Y AIS-3










