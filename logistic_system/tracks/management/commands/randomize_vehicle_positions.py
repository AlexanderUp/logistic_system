from django.core.management.base import BaseCommand

from tracks.utils import randomize_vehicle_positions


class Command(BaseCommand):
    def handle(self, *args, **options):
        tracks_created = randomize_vehicle_positions()

        self.stdout.write(
            self.style.SUCCESS(
                'Vehicle locations randomized (total {0} new tracks)'.format(
                    len(tracks_created),
                ),
            ),
        )
