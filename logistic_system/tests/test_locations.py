import pytest
from django.db.utils import IntegrityError

from locations.models import Location

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ('latitude', 'longitude'),
    [
        (0, -200),
        (0, 200),
        (-100, 0),
        (100, 0),
        (100, 200),
        (-100, -200),
    ],
)
def test_coordinates_out_of_limit(state, city, latitude, longitude):
    with pytest.raises(IntegrityError):
        assert Location.objects.create(
            city=city,
            zip_code='123456',
            latitude=latitude,
            longitude=longitude,
        )


@pytest.mark.parametrize(
    ('latitude', 'longitude'),
    [
        (0, -180),
        (0, 180),
        (-90, 0),
        (90, 0),
        (0, 0),
        (90, 180),
        (-90, -180),
    ],
)
def test_coordinates_exact_limit(state, city, latitude, longitude):
    assert Location.objects.create(
        city=city,
        zip_code='123456',
        latitude=latitude,
        longitude=longitude,
    )
