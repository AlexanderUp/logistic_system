import random
from typing import Any

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandParser

from vehicles.models import Vehicle

CARGO_CAPACITIES = (250, 500, 750, 1000)
DEFAULT_VEHICLE_CREATION_COUNT = 20


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'vehicle_count',
            nargs='?',
            type=int,
            default=DEFAULT_VEHICLE_CREATION_COUNT,
        )

    def handle(self, *args: Any, **options: Any) -> None:
        vehicle_count = options['vehicle_count']
        if vehicle_count < 1:
            raise ValidationError('Vehicle count can not be less then one.')

        vehicles = [
            Vehicle(capacity=random.choice(CARGO_CAPACITIES))
            for _ in range(vehicle_count)
        ]
        vehicles_created = Vehicle.objects.bulk_create(vehicles)

        self.stdout.write(
            self.style.SUCCESS('Vehicles created: {0}'.format(len(vehicles_created))),
        )
