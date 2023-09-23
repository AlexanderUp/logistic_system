from django.db import models
from django.utils import timezone

from locations.models import Location
from vehicles.models import Vehicle


class Track(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='tracks',
        verbose_name='location',
        help_text='Location',
    )
    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='track',
        verbose_name='vehicle',
        help_text='Vehicle',
    )
    created_at = models.DateTimeField(
        default=timezone.now(),
        verbose_name='created_at',
        help_text='Track created at',
    )

    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ('-created_at',)

    def __str__(self):
        return 'Track <{0} - {1}>'.format(self.location, self.vehicle)
