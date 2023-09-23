from django.contrib import admin

from vehicles.models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'code', 'capacity')
    search_fields = ('code__startswith',)
    empty_value_display = '--empty--'


admin.site.register(Vehicle, VehicleAdmin)
