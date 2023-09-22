import pytest
from django.db.utils import IntegrityError

from cargo.models import Cargo
from locations.models import Location

pytestmark = pytest.mark.django_db


def test_same_pickup_delivery_locations(city):
    location = Location.objects.create(
        city=city,
        zip_code='000000',
        latitude=0,
        longitude=0,
    )

    with pytest.raises(IntegrityError):
        assert Cargo.objects.create(
            weight=100,
            description='Cargo description',
            pickup_location=location,
            delivery_location=location,
        )
