import pytest

from locations.models import City, State


@pytest.fixture()
def state(faker):
    return State.objects.create(name=faker.word())


@pytest.fixture()
def city(faker, state):
    return City.objects.create(name=faker.word(), state=state)
