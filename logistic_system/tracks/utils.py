import random

from django.db import transaction

from locations.models import Location
from tracks.models import Track
from vehicles.models import Vehicle


def randomize_vehicle_positions():
    locations = Location.objects.all()
    vehicles = Vehicle.objects.all()

    with transaction.atomic():
        Track.objects.all().delete()

        tracks = []
        for vehicle in vehicles:
            tracks.append(
                Track(
                    vehicle=vehicle,
                    location=random.choice(locations),
                ),
            )

        return Track.objects.bulk_create(tracks)
