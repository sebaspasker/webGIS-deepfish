from django.db import models


class Vessel(models.Model):
    MMSI = models.CharField(max_length=9, primary_key=True)
    VesselName = models.CharField(max_length=30, null=True)
    Matricula = models.CharField(max_length=12, null=True, unique=True)

    def to_string(self):
        return (
            "Vessel MMSI: "
            + self.MMSI
            + " Name: "
            + self.VesselName
            + " Matricula: "
            + self.Matricula
        )


class AISVessel(models.Model):
    MMSI = models.ForeignKey(
        Vessel, on_delete=models.CASCADE, to_field="MMSI", related_name="MMSIOf"
    )
    BaseDateTime = models.DateTimeField()
    LAT = models.FloatField()
    LON = models.FloatField()
    SOG = models.FloatField()
    COG = models.FloatField()
    VesselName = models.CharField(max_length=30, null=True)
    CallSign = models.CharField(max_length=10)
    VesselType = models.IntegerField(null=True)
    Status = models.IntegerField(null=True)
    Length = models.IntegerField(null=True)
    Width = models.IntegerField(null=True)
    Cargo = models.IntegerField(null=True)
    TransceiverClass = models.CharField(max_length=1, null=True)

    def to_string(self):
        return (
            "MMSI: "
            + str(self.MMSI.MMSI)
            + " Vessel Name: "
            + self.VesselName
            + " LON: "
            + str(self.LON)
            + " LAT: "
            + str(self.LAT)
        )


class Plate(models.Model):
    Lote = models.CharField(max_length=15, null=False, primary_key=True)
    Matricula = models.ForeignKey(
        Vessel,
        on_delete=models.CASCADE,
        to_field="Matricula",
        related_name="MatriculaOf",
    )
    Puerto = models.CharField(max_length=30, null=True)
    Zona_Captura = models.CharField(max_length=7, null=True)
    Fecha_Inicio = models.DateTimeField()
    Fecha_Fin = models.DateTimeField()
    Nombre_Pez_Bandeja = models.CharField(max_length=20, null=True)
    Kg_Bandeja = models.IntegerField(null=True)


class Fish(models.Model):
    Nombre_Cientifico = models.CharField(max_length=30, primary_key=True)
    Nombre_Comercial = models.CharField(max_length=30)


# Fish analysis in each plate
class Fish_Plate(models.Model):
    Lote = models.ForeignKey(
        Plate, on_delete=models.CASCADE, to_field="Lote", related_name="LoteOf"
    )
    Nombre_Cientifico = models.ForeignKey(
        Fish, on_delete=models.CASCADE, to_field="Nombre_Cientifico"
    )
    Talla_cm = models.IntegerField()
    Cantidad = models.IntegerField()
    Peso = models.FloatField(null=True)


# Relation to easy search
class Travel(models.Model):
    Vessel_fk = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    AIS_fk = models.ForeignKey(AISVessel, on_delete=models.CASCADE)
    Plate_fk = models.ForeignKey(Plate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("Vessel_fk", "AIS_fk", "Plate_fk")

    def to_string(self):
        return (
            "Travel with AIS:("
            + AIS_fk.id
            + ") Vessel:("
            + Vessel_fk.id
            + ") Plate:("
            + Plate_kf.id
            + ")"
        )
