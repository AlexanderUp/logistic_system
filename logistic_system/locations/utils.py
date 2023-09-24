from geopy import distance

from locations.models import Location


def distance_between_locations(
    departure_point: Location,
    destination_point: Location,
) -> float:
    return distance.distance(
        departure_point.coordinates,
        destination_point.coordinates,
    ).miles
