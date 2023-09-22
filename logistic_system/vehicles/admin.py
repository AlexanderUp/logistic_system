from django.contrib import admin

from vehicles.models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'capacity')
    empty_value_display = '--empty--'


admin.site.register(Vehicle, VehicleAdmin)
