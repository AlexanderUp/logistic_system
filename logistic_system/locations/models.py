from django.db import models

LATITUDE_NORTH_VALUE_LIMIT: int = 90
LATITUDE_SOUTH_VALUE_LIMIT: int = -90
LONGITUDE_EAST_VALUE_LIMIT: int = 180
LONGITUDE_WEST_VALUE_LIMIT: int = -180


class State(models.Model):
    state_id = models.CharField(
        max_length=2,
        unique=True,
        verbose_name='state_id',
        help_text='2-letter ID of state',
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='name',
        help_text='Name of state',
    )

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'
        ordering = ('-pk',)

    def __str__(self):
        return f'State <{self.name}>'


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='name',
        help_text='Name of city',
    )
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name='state',
        help_text='State in which city placed',
    )

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('-pk',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'state'),
                name='unique_city_state',
            ),
        )

    def __str__(self):
        return 'City <{0} ({1})>'.format(self.name, self.state.name)


class Location(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name='city',
        help_text='City where location placed',
    )
    zip_code = models.CharField(
        max_length=6,
        unique=True,
        verbose_name='zip_code',
        help_text='Zip code of location',
    )
    latitude = models.FloatField(
        verbose_name='latitude',
        help_text='Latitude',
    )
    longitude = models.FloatField(
        verbose_name='longitude',
        help_text='Logitude',
    )

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ('-pk',)
        constraints = (
            models.CheckConstraint(
                check=(
                    models.Q(latitude__gte=LATITUDE_SOUTH_VALUE_LIMIT)
                    & models.Q(latitude__lte=LATITUDE_NORTH_VALUE_LIMIT)
                ),
                name='latitude_value_constraint',
            ),
            models.CheckConstraint(
                check=(
                    models.Q(longitude__gte=LONGITUDE_WEST_VALUE_LIMIT)
                    & models.Q(longitude__lte=LONGITUDE_EAST_VALUE_LIMIT)
                ),
                name='longitude_value_constraint',
            ),
        )

    def __str__(self):
        return 'Location <{0} ({1}, {2})>'.format(
            self.zip_code,
            self.city.name,
            self.city.state.name,
        )
