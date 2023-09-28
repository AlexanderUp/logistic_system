from django.contrib import admin

from tracks.models import Track


class TrackAdmin(admin.ModelAdmin):
    list_display = ('pk', 'location', 'vehicle', 'created_at')
    raw_id_fields = ('location', 'vehicle')
    empty_value_display = '--empty--'


admin.site.register(Track, TrackAdmin)
