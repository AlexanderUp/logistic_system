from django.conf import settings
from geopy import distance
from rest_framework import serializers

from api.utils import annotate_vehicle
from cargo.models import Cargo
from locations.models import Location
from vehicles.models import Vehicle


class VehicleNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'code',
        ]


class CargoBaseSerializer(serializers.ModelSerializer):
    pickup_location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.select_related('city', 'city__state'),
    )
    delivery_location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.select_related('city', 'city__state'),
    )
    vehicle_assigned = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Vehicle.objects.all(),
        allow_null=True,
        default=None,
    )

    class Meta:
        model = Cargo
        fields = [
            'pk',
            'weight',
            'pickup_location',
            'delivery_location',
            'description',
            'vehicle_assigned',
        ]

    def validate(self, data):
        if data['pickup_location'] == data['delivery_location']:
            raise serializers.ValidationError('Delivery to same location prohibited!')
        vehicle_assigned = data.pop('vehicle_assigned')
        data['vehicle'] = vehicle_assigned
        return data


class CargoListSerializer(CargoBaseSerializer):
    closest_vehicles_count = serializers.SerializerMethodField()

    class Meta(CargoBaseSerializer.Meta):
        model = Cargo
        fields = CargoBaseSerializer.Meta.fields + [
            'closest_vehicles_count',
        ]

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


class VehicleDistanceSerializer(VehicleNestedSerializer):
    distance_to = serializers.SerializerMethodField()

    class Meta(VehicleNestedSerializer.Meta):
        fields = VehicleNestedSerializer.Meta.fields + [
            'distance_to',
        ]

    def get_distance_to(self, obj):
        return obj.distance_to


class CargoDetailSerializer(CargoBaseSerializer):
    vehicles = serializers.SerializerMethodField()

    class Meta(CargoBaseSerializer.Meta):
        fields = CargoBaseSerializer.Meta.fields + [
            'vehicles',
        ]

    def get_vehicles(self, obj):
        vehicles_qs = self.context['vehicles_qs']
        distances = (
            distance.distance(
                (vehicle.current_lat, vehicle.current_long),
                obj.pickup_location.coordinates,
            ).miles
            for vehicle in vehicles_qs
        )
        vehicles = [
            annotate_vehicle(vehicle, distance_to)
            for vehicle, distance_to in zip(vehicles_qs, distances)
        ]
        return VehicleDistanceSerializer(vehicles, many=True).data
