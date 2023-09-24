from django.conf import settings
from geopy import distance
from rest_framework import serializers

from cargo.models import Cargo
from locations.models import Location
from vehicles.models import Vehicle


class CargoSerializer(serializers.ModelSerializer):
    pickup_location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.select_related('city', 'city__state'),
    )
    delivery_location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.select_related('city', 'city__state'),
    )
    vehicle = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Vehicle.objects.all(),
        allow_null=True,
        default=None,
    )
    closest_vehicles_count = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = (
            'pk',
            'weight',
            'pickup_location',
            'delivery_location',
            'description',
            'vehicle',
            'closest_vehicles_count',
        )

    def validate(self, data):
        if data['pickup_location'] == data['delivery_location']:
            raise serializers.ValidationError('Delivery to same location prohibited!')

    def get_closest_vehicles_count(self, obj):
        vehicles = self.context['vehicles_qs']
        return len(
            [
                vehicle
                for vehicle in vehicles
                if distance.distance(
                    (vehicle.current_lat, vehicle.current_long),
                    obj.pickup_location.coordinates,
                ).miles
                <= settings.CLOSEST_VEHICLE_RANGE_IN_MILES
            ],
        )
