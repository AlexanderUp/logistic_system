from django.contrib import admin

from locations.models import City, Location, State


class StateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'state_id', 'name')
    empty_value_display = '--empty--'


class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'state')
    empty_value_display = '--empty--'


class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'state', 'city', 'zip_code', 'latitude', 'longitude')
    empty_value_display = '--empty--'


admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Location, LocationAdmin)
