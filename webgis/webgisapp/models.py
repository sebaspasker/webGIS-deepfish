from django.db import models


class Vessel(models.Model):
    MMSI = models.CharField(max_length=9, primary_key=True)
    VesselName = models.CharField(max_length=30, null=True)
    Matricula = models.CharField(max_length=12, null=True, unique=True)
    Image = models.CharField(max_length=20, null=True)

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


# Añadir timestamp
class Plate(models.Model):
    # Cambiar que sea el timestamp de la imagen
    Timestamp = models.DateTimeField(primary_key=True, auto_now_add=True)
    Lote = models.CharField(
        max_length=15,
        null=False,
    )
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

    def to_string(self):
        return (
            "\n\nLote: "
            + self.Lote
            + " Matricula: "
            + self.Matricula.Matricula
            + " Timestamp: "
            + self.Timestamp
            + "\n--------------------------------\n"
            + "Puerto: "
            + str(self.Puerto)
            + " Zona captura: "
            + str(self.Zona_Captura)
            + "\nPez: "
            + str(self.Nombre_Pez_Bandeja)
            + " Kg: "
            + str(self.Kg_Bandeja)
            + "\n................................\n"
            + "Fecha inicio: "
            + str(self.Fecha_Inicio)
            + "\nFecha fin: "
            + str(self.Fecha_Fin)
            + "\n________________________________\n"
        )


class Fish(models.Model):
    Nombre_Cientifico = models.CharField(max_length=30, primary_key=True)
    Nombre_Comercial = models.CharField(max_length=30)


# Fish analysis in each plate
# Quitar la cantidad
class Fish_Plate(models.Model):
    Plate = models.ForeignKey(Plate, on_delete=models.CASCADE)
    Nombre_Cientifico = models.ForeignKey(
        Fish, on_delete=models.CASCADE, to_field="Nombre_Cientifico"
    )
    Talla_cm = models.FloatField()
    Peso = models.FloatField()


# Relation to easy search
class Travel(models.Model):
    Vessel_fk = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    AIS_fk = models.ForeignKey(AISVessel, on_delete=models.CASCADE)
    Plate_fk = models.ForeignKey(Plate, on_delete=models.CASCADE, to_field="Timestamp")
    KG = models.FloatField(null=True)

    class Meta:
        unique_together = ("Vessel_fk", "AIS_fk", "Plate_fk")

    def to_string(self):
        return (
            "Travel with AIS: ("
            + AIS_fk.id
            + ") Vessel: ("
            + Vessel_fk.id
            + ") Plate: ("
            + Plate_fk.id
            + ")"
        )


class Travel_Fish(models.Model):
    Travel_fk = models.ForeignKey(Travel, on_delete=models.CASCADE)
    Nombre_Cientifico = models.ForeignKey(
        Fish, on_delete=models.CASCADE, to_field="Nombre_Cientifico"
    )
    KG = models.FloatField(null=True)
