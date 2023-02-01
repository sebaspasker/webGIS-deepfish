from webgisapp.models import AISVessel, Vessel, Plate, Travel


def allAIS():
    return AISVessel.objects.all()


def allVessels():
    return Vessel.objects.all()


def allPlates():
    return Plate.objects.all()


def allTravels():
    return Travel.objects.all()


# def comparison(func, *args):
#     for i in len(args):
