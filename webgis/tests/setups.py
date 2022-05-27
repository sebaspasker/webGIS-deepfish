import pytest
from datetime import datetime, timedelta
import datetime
from webgisapp.models import *
from geojson import Point, LineString, MultiPoint, Feature, FeatureCollection


def setupTestRelateAISKg(self):
    self.v1 = Vessel.objects.create(
        MMSI="123456789", VesselName="Juan", Matricula="M123"
    )

    self.v2 = Vessel.objects.create(
        MMSI="987654321", VesselName="Jorge", Matricula="A321"
    )

    date = datetime.datetime.now()
    self.ais1 = AISVessel.objects.create(
        MMSI=self.v1,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.ais2 = AISVessel.objects.create(
        MMSI=self.v2,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v2.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.plate1 = Plate.objects.create(
        Lote="ABC",
        Matricula=self.v1,
        Puerto="Campello",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )

    self.plate2 = Plate.objects.create(
        Lote="CBD",
        Matricula=self.v2,
        Puerto="Torrevieja",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )

    self.fish_plate1 = Fish_Plate.objects.create(
        Lote=self.plate1,
        Nombre_Cientifico=self.p,
        Talla_cm=2,
        Cantidad=2,
        Peso=2,
    )

    self.fish_plate2 = Fish_Plate.objects.create(
        Lote=self.plate2,
        Nombre_Cientifico=self.p,
        Talla_cm=2,
        Cantidad=2,
        Peso=2,
    )

    self.travel1 = Travel.objects.create(
        AIS_fk=self.ais1, Vessel_fk=self.v1, Plate_fk=self.plate1
    )

    self.travel2 = Travel.objects.create(
        AIS_fk=self.ais2, Vessel_fk=self.v2, Plate_fk=self.plate2
    )


def setupTestComprobePossibleJoin(self):
    setupTestDeleteTravel(self)


def setupTestComprobeOutdatedTravel(self):
    setupTestDeleteTravel(self)


def setupTestDeleteTravel(self):
    self.v1 = Vessel.objects.create(
        MMSI="123456789", VesselName="Juan", Matricula="M123"
    )

    self.v2 = Vessel.objects.create(
        MMSI="987654321", VesselName="Jorge", Matricula="A321"
    )

    date = datetime.datetime.now()
    self.ais1 = AISVessel.objects.create(
        MMSI=self.v1,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.ais2 = AISVessel.objects.create(
        MMSI=self.v2,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v2.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.plate1 = Plate.objects.create(
        Lote="ABC",
        Matricula=self.v1,
        Puerto="Campello",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )

    self.plate2 = Plate.objects.create(
        Lote="CBD",
        Matricula=self.v2,
        Puerto="Torrevieja",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )

    self.travel1 = Travel.objects.create(
        AIS_fk=self.ais1, Vessel_fk=self.v1, Plate_fk=self.plate1
    )

    self.travel2 = Travel.objects.create(
        AIS_fk=self.ais2, Vessel_fk=self.v2, Plate_fk=self.plate2
    )


def setupTestJoinTravel(self):
    self.v1 = Vessel.objects.create(
        MMSI="123456789", VesselName="Juan", Matricula="M123"
    )

    self.v2 = Vessel.objects.create(
        MMSI="987654321", VesselName="Jorge", Matricula="A321"
    )

    date = datetime.datetime.now()
    self.ais1 = AISVessel.objects.create(
        MMSI=self.v1,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.ais2 = AISVessel.objects.create(
        MMSI=self.v2,
        BaseDateTime=date,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=self.v2.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.plate1 = Plate.objects.create(
        Lote="ABC",
        Matricula=self.v1,
        Puerto="Campello",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )

    self.plate2 = Plate.objects.create(
        Lote="CBD",
        Matricula=self.v2,
        Puerto="Torrevieja",
        Zona_Captura="AB",
        Fecha_Inicio=date - timedelta(minutes=5),
        Fecha_Fin=date + timedelta(minutes=5),
        Nombre_Pez_Bandeja=date + timedelta(minutes=5),
        Kg_Bandeja=2,
    )


def setupTestAISQuery(self):
    v1 = Vessel.objects.create(MMSI="123456789", VesselName="Juan", Matricula="M123")

    v2 = Vessel.objects.create(MMSI="987654321", VesselName="Jorge", Matricula="A321")

    ais1 = AISVessel.objects.create(
        MMSI=v1,
        BaseDateTime=datetime.datetime.now(),
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    ais2 = AISVessel.objects.create(
        MMSI=v2,
        BaseDateTime=datetime.datetime.now(),
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.collection = FeatureCollection(
        [
            Feature(
                geometry=Point([(ais1.LON, ais1.LAT)]),
                properties={
                    "MMSI": v1.MMSI,
                    "VesselName": v1.VesselName,
                    "Matricula": v1.Matricula,
                    "Color": "#fe0000",  # Red
                },
            ),
            Feature(
                geometry=Point([(ais2.LON, ais2.LAT)]),
                properties={
                    "MMSI": v2.MMSI,
                    "VesselName": v2.VesselName,
                    "Matricula": v2.Matricula,
                    "Color": "#fe4600",  # Red Orange
                },
            ),
        ]
    )

    self.collection2 = FeatureCollection(
        [
            Feature(
                geometry=Point([(float(ais1.LON), float(ais1.LAT))]),
                properties={
                    "MMSI": v1.MMSI,
                    "VesselName": v1.VesselName,
                    "Matricula": v1.Matricula,
                    "Color": "#fe0000",  # Red
                },
            ),
            Feature(
                geometry=Point([(float(ais2.LON), float(ais2.LAT))]),
                properties={
                    "MMSI": v2.MMSI,
                    "VesselName": v2.VesselName,
                    "Matricula": v2.Matricula,
                    "Color": "#fe4600",  # Red Orange
                },
            ),
        ]
    )


def setupFilterType(self):
    v1 = Vessel.objects.create(MMSI="123456789", VesselName="Juan", Matricula="M123")

    v2 = Vessel.objects.create(MMSI="987654321", VesselName="Jorge", Matricula="A321")

    ais1 = AISVessel.objects.create(
        MMSI=v1,
        BaseDateTime=datetime.datetime.now(),
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    ais2 = AISVessel.objects.create(
        MMSI=v2,
        BaseDateTime=datetime.datetime.now(),
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName=v1.VesselName,
        CallSign="ABC",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.collection = FeatureCollection(
        [
            Feature(
                geometry=MultiPoint([(ais1.LON, ais1.LAT)]),
                properties={
                    "MMSI": v1.MMSI,
                    "VesselName": v1.VesselName,
                    "Matricula": v1.Matricula,
                    "Color": "#fe0000",  # Red
                },
            ),
            Feature(
                geometry=MultiPoint([(ais2.LON, ais2.LAT)]),
                properties={
                    "MMSI": v2.MMSI,
                    "VesselName": v2.VesselName,
                    "Matricula": v2.Matricula,
                    "Color": "#fe4600",  # Red Orange
                },
            ),
        ]
    )

    self.collection2 = FeatureCollection(
        [
            Feature(
                geometry=LineString([(ais1.LON, ais1.LAT)]),
                properties={
                    "MMSI": v1.MMSI,
                    "VesselName": v1.VesselName,
                    "Matricula": v1.Matricula,
                    "Color": "#fe0000",  # Red
                },
            ),
            Feature(
                geometry=LineString([(ais2.LON, ais2.LAT)]),
                properties={
                    "MMSI": v2.MMSI,
                    "VesselName": v2.VesselName,
                    "Matricula": v2.Matricula,
                    "Color": "#fe4600",  # Red Orange
                },
            ),
        ]
    )

    self.collection3 = FeatureCollection(
        [
            Feature(
                geometry=MultiPoint([(float(ais1.LON), float(ais1.LAT))]),
                properties={
                    "MMSI": v1.MMSI,
                    "VesselName": v1.VesselName,
                    "Matricula": v1.Matricula,
                    "Color": "#fe0000",  # Red
                    "Weight": 0.0,
                },
            ),
            Feature(
                geometry=MultiPoint([(float(ais2.LON), float(ais2.LAT))]),
                properties={
                    "MMSI": v2.MMSI,
                    "VesselName": v2.VesselName,
                    "Matricula": v2.Matricula,
                    "Color": "#fe4600",  # Red Orange
                    "Weight": 0.0,
                },
            ),
        ]
    )


def setupFilterRoute(self):
    self.p = Fish.objects.create(Nombre_Cientifico="Pez1", Nombre_Comercial="Pez1")

    self.v = Vessel.objects.create(MMSI="ABCDEF", VesselName="Juan", Matricula="Buque")
    time_init = datetime.datetime.now()
    self.ais1 = AISVessel.objects.create(
        MMSI=self.v,
        BaseDateTime=time_init,
        LAT=1,
        LON=1,
        SOG=1,
        COG=1,
        VesselName="Juan",
        CallSign="12",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.ais2 = AISVessel.objects.create(
        MMSI=self.v,
        BaseDateTime=time_init,
        LAT=2,
        LON=2,
        SOG=2,
        COG=2,
        VesselName="Juan",
        CallSign="12",
        VesselType=1,
        Status=1,
        Length=1,
        Width=1,
        Cargo=1,
        TransceiverClass="A",
    )

    self.plate = Plate.objects.create(
        Lote="Lote1",
        Matricula=self.v,
        Puerto="Campello",
        Zona_Captura="AB1",
        Fecha_Inicio=time_init,
        Fecha_Fin=time_init + timedelta(minutes=5),
        Nombre_Pez_Bandeja="Bonito como tu",
        Kg_Bandeja=2,
    )

    self.fish_plate = Fish_Plate.objects.create(
        Lote=self.plate,
        Nombre_Cientifico=self.p,
        Talla_cm=2,
        Cantidad=2,
        Peso=2,
    )
