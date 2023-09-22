import functools

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from vehicles.utils import generate_random_code


class Vehicle(models.Model):
    code = models.CharField(
        max_length=5,
        unique=True,
        default=functools.partial(generate_random_code),
        verbose_name='code',
        help_text='Unique code of vehicle',
    )
    capacity = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(1000)),
        default=100,
        verbose_name='capacity',
        help_text='Cargo carrying capacity of the vehicle',
    )

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'
        ordering = ('-pk',)

    def __str__(self):
        return f'Vehicle <{self.code}>'
