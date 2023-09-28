import random

from django.core.management.base import BaseCommand
from django.db import transaction

from locations.models import Location
from tracks.models import Track
from vehicles.models import Vehicle


class Command(BaseCommand):
    def handle(self, *args, **options):
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

            tracks_created = Track.objects.bulk_create(tracks)

        self.stdout.write(
            self.style.SUCCESS(
                'Vehicle locations randomized (total {0} new tracks)'.format(
                    len(tracks_created),
                ),
            ),
        )
