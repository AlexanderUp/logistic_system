from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CargoViewSet

v1_router = DefaultRouter()
v1_router.register('cargoes', CargoViewSet, basename='cargo')

app_name = 'api'

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
