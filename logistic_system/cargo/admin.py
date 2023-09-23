from django.contrib import admin

from cargo.models import Cargo


class CargoAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'weight',
        'pickup_location',
        'delivery_location',
        'description',
        'vehicle',
    )
    raw_id_fields = ('pickup_location', 'delivery_location')
    empty_value_display = '--empty--'


admin.site.register(Cargo, CargoAdmin)
