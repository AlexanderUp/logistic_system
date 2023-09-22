import pytest

from locations.models import City, State


@pytest.fixture()
def state():
    return State.objects.create(name='Alaska')


@pytest.fixture()
def city(state):
    return City.objects.create(name='Anchorage', state=state)
