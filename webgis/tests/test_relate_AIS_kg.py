import pytest
from .setups import setupTestRelateAISKg

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestRelateAISKg:
    pytestmark = pytest.mark.django_db

    def setup(self):
        pass
        # setupTestRelateAISKg(self)

    def testTravelsInstance(self):
        # TODO
        pass

    def testTravelsNone(self):
        # TODO
        pass

    def testSpecieInstance(self):
        # TODO
        pass

    def testNameSpecieInstance(self):
        # TODO
        pass

    def testSpecieNone(self):
        # TODO
        pass

    def testNameSpecieNoneAndSpecieTrue(self):
        # TODO
        pass

    def testTravelDictKgCorrect(self):
        # TODO
        pass

    def testTravelDictKgEmpty(self):
        # TODO
        pass

    def testTravelDictOneTravelQuerySet(self):
        # TODO
        pass

    def testTravelDictTravelEmptyWeight(self):
        # TODO
        pass
