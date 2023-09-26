from vehicles.models import Vehicle


def annotate_vehicle(vehicle: Vehicle, distance_to: float) -> Vehicle:
    vehicle.__dict__['distance_to'] = distance_to
    return vehicle
