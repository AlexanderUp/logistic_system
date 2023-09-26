from django.db.models import OuterRef, Subquery
from rest_framework import viewsets

from api.serializers import CargoDetailSerializer, CargoListSerializer, VehicleSerializer
from cargo.models import Cargo
from tracks.models import Track
from vehicles.models import Vehicle


class CargoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Cargo.objects.select_related(
            'pickup_location',
            'delivery_location',
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        track_qs = Track.objects.filter(vehicle=OuterRef('pk'))
        vehicles_qs = Vehicle.objects.annotate(
            current_lat=Subquery(track_qs.values('location__latitude')[:1]),
            current_long=Subquery(track_qs.values('location__longitude')[:1]),
        )
        context['vehicles_qs'] = vehicles_qs
        return context

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CargoDetailSerializer
        return CargoListSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        track_qs = Track.objects.filter(vehicle=OuterRef('pk'))
        return Vehicle.objects.annotate(
            current_location=Subquery(track_qs.values('location__zip_code')[:1]),
        )
