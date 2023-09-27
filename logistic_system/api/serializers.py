from django.conf import settings
from geopy import distance
from rest_framework import serializers

from api.utils import annotate_vehicle_with_distance
from cargo.models import Cargo
from locations.models import Location
from tracks.models import Track
from vehicles.models import Vehicle


class VehicleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'pk',
            'code',
        ]


class VehicleSerializer(VehicleBaseSerializer):
    current_location = serializers.SerializerMethodField()

    class Meta(VehicleBaseSerializer.Meta):
        fields = VehicleBaseSerializer.Meta.fields + [
            'current_location',
            'capacity',
        ]

    def get_current_location(self, obj):
        return obj.current_location


class VehicleDistanceSerializer(VehicleBaseSerializer):
    distance_to = serializers.SerializerMethodField()

    class Meta(VehicleBaseSerializer.Meta):
        fields = VehicleBaseSerializer.Meta.fields + [
            'distance_to',
        ]

    def get_distance_to(self, obj):
        return obj.distance_to


class CargoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['pk', 'weight', 'description']


class CargoSerializer(CargoBaseSerializer):
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
    )

    class Meta(CargoBaseSerializer.Meta):
        fields = CargoBaseSerializer.Meta.fields + [
            'pickup_location',
            'delivery_location',
            'vehicle',
        ]

    def validate(self, data):
        if data['pickup_location'] == data['delivery_location']:
            raise serializers.ValidationError('Delivery to same location prohibited!')
        return data


class CargoListSerializer(CargoSerializer):
    closest_vehicles_count = serializers.SerializerMethodField()

    class Meta(CargoSerializer.Meta):
        fields = CargoSerializer.Meta.fields + [
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


class CargoDetailSerializer(CargoSerializer):
    vehicles = serializers.SerializerMethodField()

    class Meta(CargoSerializer.Meta):
        fields = CargoSerializer.Meta.fields + [
            'vehicles',
        ]

    def get_vehicles(self, obj):
        vehicles_qs = self.context['vehicles_qs']
        vehicle_distances = (
            (
                vehicle,
                distance.distance(
                    (vehicle.current_lat, vehicle.current_long),
                    obj.pickup_location.coordinates,
                ).miles,
            )
            for vehicle in vehicles_qs
        )
        vehicles = [
            annotate_vehicle_with_distance(vehicle, distance_to)
            for vehicle, distance_to in vehicle_distances
        ]
        return VehicleDistanceSerializer(vehicles, many=True).data


class TrackSerializer(serializers.ModelSerializer):
    vehicle = serializers.SlugRelatedField(
        slug_field='code',
        queryset=Vehicle.objects.all(),
    )
    location = serializers.SlugRelatedField(
        slug_field='zip_code',
        queryset=Location.objects.select_related('city__state'),
    )

    class Meta:
        model = Track
        fields = ('vehicle', 'location')

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        location = validated_data['location']
        track, _ = Track.objects.get_or_create(vehicle=vehicle)
        track.location = location
        track.save()
        return track
