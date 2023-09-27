from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CargoViewSet, TrackViewset, VehicleViewSet

v1_router = DefaultRouter()
v1_router.register('cargoes', CargoViewSet, basename='cargo')
v1_router.register('vehicles', VehicleViewSet, basename='vehicle')
v1_router.register('tracks', TrackViewset, basename='track')


app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
