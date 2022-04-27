from django.db import models

class Vessel(models.Model):
    MMSI = models.CharField(max_length=9, primary_key=True)
    VesselName = models.CharField(max_length=30, null=True)

class AISVessel(models.Model):
    id = models.BigAutoField(primary_key=True)
    MMSI = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    BaseDateTime = models.DateField()
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
