from django.db.models import OuterRef, Subquery
from rest_framework import viewsets

from api.serializers import CargoSerializer
from cargo.models import Cargo
from tracks.models import Track
from vehicles.models import Vehicle


class CargoViewSet(viewsets.ModelViewSet):
    serializer_class = CargoSerializer

    def get_queryset(self):
        return Cargo.objects.select_related(
            'pickup_location',
            'delivery_location',
            'pickup_location__city',
            'delivery_location__city',
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        vehicles_qs = Vehicle.objects.annotate(
            current_lat=Subquery(
                Track.objects.filter(vehicle=OuterRef('pk')).values(
                    'location__latitude',
                )[:1],
            ),
            current_long=Subquery(
                Track.objects.filter(vehicle=OuterRef('pk')).values(
                    'location__longitude',
                )[:1],
            ),
        )
        context['vehicles_qs'] = vehicles_qs
        return context
