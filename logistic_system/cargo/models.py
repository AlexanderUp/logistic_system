from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from locations.models import Location
from vehicles.models import Vehicle


class Cargo(models.Model):
    weight = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(1000)),
        verbose_name='weight',
        help_text='Cargo weight',
    )
    pickup_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='pickup_locations',
        verbose_name='pickup_location',
        help_text='Cargo pick-up location',
    )
    delivery_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='delivery_locations',
        verbose_name='delivery_location',
        help_text='Cargo delivery location',
    )
    description = models.CharField(
        max_length=1000,
        verbose_name='description',
        help_text='Cargo description',
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='cargoes',
        blank=True,
        null=True,
        verbose_name='vehicle',
        help_text='Transporting vehicle',
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargoes'
        ordering = ('-pk',)
        constraints = (
            models.CheckConstraint(
                check=~models.Q(delivery_location=models.F('pickup_location')),
                name='same_pickup_delivery_location_constraint',
            ),
        )

    def __str__(self):
        return 'Cargo <{0} ({1})>'.format(self.weight, self.pk)
