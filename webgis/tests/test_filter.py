import pytest
from geojson import Point, LineString, MultiPoint
from webgisapp.utils.exceptions import *
from webgisapp.utils.abbr import *
from webgisapp.utils.filter import Filter_Type, Filter_Route

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestFilterType():
    pytestmark = pytest.mark.django_db
    collection = ""

    # Input: TypeStr, Vessels, AIS
    # Ouput: collection, route, typee

    def setup():
        v1 = Vessel.objects.create(
            MMSI = "123456789",
            VesselName="Juan",
            Matricula="M123"
        )

        v2 = Vessel.objects.create(
            MMSI = "987654321",
            VesselName="Jorge",
            Matricula="A321"
        )

        ais1 = AISVessel.objects.create(
            MMSI = v1,
            BaseDateTime = datetime.datetime.now(),
            LAT=1,
            LON=1,
            SOG=1,
            COG=1,
            VesselName=v1.VesselName,
            CallSign='ABC',
            VesselType=1,
            Status=1,
             Length=1,
            Width=1,
            Cargo=1,
            TransceiverClass='A'
        )

        ais2 = AISVessel.objects.create(
            MMSI = v2,
            BaseDateTime = datetime.datetime.now(),
            LAT=1,
            LON=1,
            SOG=1,
            COG=1,
            VesselName=v1.VesselName,
            CallSign='ABC',
            VesselType=1,
            Status=1,
            Length=1,
            Width=1,
            Cargo=1,
            TransceiverClass='A'
        )

        self.collection = FeatureCollection(
            [
                Feature(
                    geometry = Point([(ais1.LON, ais1.LAT)]),
                    properties = {
                        'MMSI': v1.MMSI,
                        'VesselName' : v1.VesselName,
                        'Matricula' : v1.Matricula,
                        'Color' : "#fe0000", # Red
                    }),
                Feature(
                    geometry = Point([(ais2.LON, ais2.LAT)]),
                    properties = {
                        'MMSI': v2.MMSI,
                        'VesselName' : v2.VesselName,
                        'Matricula' : v2.Matricula,
                        'Color' : "#fe4600", # Red Orange
                }),
            ]
           )


    def testNoneStr():
        try:
            Filter_Type(None, allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, EmptyVarException)

    def testOtherTypeStr():
        try:
            Filter_Type(2, allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, InstanceTypeException)


    def testStrEmpty():
        try:
            Filter_Type("", allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, EmptyVarException)

    def testStrDifferent():
        try:
            Filter_Type("Random", allVessels(), allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, IncorrectOptionException)

    def testNotVessel():
        try:
            Filter_Type("Point", "", allAIS())
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, InstanceTypeException)

    def testNotAIS():
        try:
            Filter_Type("Point", allVessels(), "")
            assert False, "Debería de saltar una excepción"
        except Exception as e:
            assert isinstance(e, InstanceTypeException)

    def testPointType():
        # TODO
        collection, route, typee = Filter_Type("Point", allVessels(), allAIS())
        assert False
        

    def testLineStringType():
        # TODO
        collection, route, typee = Filter_Type("Line", allVessels(), allAIS())
        assert False

    def testPointAndLineType():
        # TODO
        collection, route, typee = Filter_Type("PointAndLine", allVessels(), allAIS())
        assert False


    def testHeatType():
        # TODO
        collection, route, typee = Filter_Type("Heat", allVessels(), allAIS())
        assert False
