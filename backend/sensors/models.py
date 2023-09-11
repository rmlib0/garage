from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('tag'),
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name=_('color'),
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['id']

    def __str__(self):
        return self.name


# class SensorType(models.Model):
#     CHOICES = (
#         ('PIR', 'Passive infrared motion sensor'),
#         ('LDR', 'Light Dependent Resistor'),
#         ('DHT', 'Temperature and humidity sensor'),
#         ('PS', 'Pressure sensor'),
#     )
#     type = models.CharField(
#         max_length=300,
#         choices=CHOICES
#     )

#     class Meta:
#         verbose_name = 'Sensor type'
#         verbose_name_plural = 'Sensor types'
#         ordering = ['id']

#     def get_full_name(self, sensor_type: str) -> str:
#         return {
#             'PIR': 'Passive infrared motion sensor',
#             'LDR': 'Light Dependent Resistor',
#             'DHT': 'Temperature and humidity sensor',
#             'PS': 'Pressure sensor',
#         }.get(sensor_type)

#     def __str__(self):
#         return f'{self.type} : {self.get_full_name(self.type)}'


# class Sensor(models.Model):
#     name = models.CharField(
#         verbose_name=_('name'),
#         max_length=200
#     )
#     sensor_type = models.ForeignKey(
#         SensorType,
#         verbose_name=_('sensor type'),
#         on_delete=models.CASCADE,
#         related_name='sensors'
#     )


class ModelWithDescription(models.Model):
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class Manufacturer(ModelWithDescription):
    name = models.CharField(
        verbose_name=_('manufacturer name'),
        unique=True,
        max_length=255
    )
    country = CountryField(
        verbose_name=_('country')
    )
    url = models.URLField(
        verbose_name=_('manufacturer web-site'),
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Manufacturer'
        verbose_name_plural = 'Manufacturers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Garage(ModelWithDescription):
    name = models.CharField(
        verbose_name=_('garage name'),
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Garage'
        verbose_name_plural = 'Garages'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Floor(ModelWithDescription):
    name = models.CharField(
        verbose_name=_('floor name'),
        max_length=200
    )
    garage = models.ForeignKey(
        Garage,
        on_delete=models.CASCADE,
        related_name='floors'
    )

    class Meta:
        verbose_name = 'Floor'
        verbose_name_plural = 'Floors'
        ordering = ['garage', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'garage'],
                name='unique_floor'
            )
        ]

    def __str__(self):
        return f'{self.name} in № {self.garage.name} garage'


class Room(ModelWithDescription):
    name = models.CharField(
        verbose_name='Room',
        max_length=200
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    # sensors = models.ForeignKey(
    #     Sensor,
    #     on_delete=models.CASCADE,
    #     verbose_name=_('sensors'),
    # )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='rooms',
        blank=True
    )

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['name']

    def __str__(self):
        return (
            f'Room: {self.name} is suited on {self.floor.name}'
            f'at garage {self.floor.garage.name}'
        )


class Sensor(ModelWithDescription):
    SENSOR_TYPES = (
        ('DHT', 'Temperature and humidity'),
        ('PIR', 'Motin detection'),
        ('PR', 'Pressure sensor'),
    )
    status = models.BooleanField(
        verbose_name=_('active'),
        default=True
    )
    name = models.CharField(
        verbose_name=_('sensor name'),
        max_length=255
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    type = models.CharField(
        verbose_name=_('sensor type'),
        max_length=3,
        choices=SENSOR_TYPES
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='sensors',
        related_query_name='sensors'
    )

    class Meta:
        pass

    def __str__(self):
        return (f'Sensor: {self.type} -> {self.get_type_display()}'
                f' -- {self.name} in {self.room.name}')


class DHT(Sensor):
    temperature = models.FloatField(
        'Temperature',
        blank=True,
        null=True
    )
    humidity = models.FloatField(
        'Humidity',
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        verbose_name=_('action timestamp'),
        auto_now_add=True
    )


class PIR(Sensor):
    detection = models.BooleanField(
        verbose_name=_('motion detection')
    )
    action_timestamp = models.DateTimeField(
        verbose_name=_('action timestamp'),
        auto_now_add=True
    )


class PR(Sensor):
    pressure = models.FloatField(
        'Pressure')
