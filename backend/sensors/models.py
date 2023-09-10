from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

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


class SensorType(models.Model):
    CHOICES = (
        ('PIR', 'Passive infrared motion sensor'),
        ('LDR', 'Light Dependent Resistor'),
        ('DHT', 'Temperature and humidity sensor'),
        ('PS', 'Pressure sensor'),
    )
    type = models.CharField(
        max_length=300,
        choices=CHOICES
    )

    class Meta:
        verbose_name = 'Sensor type'
        verbose_name_plural = 'Sensor types'
        ordering = ['id']

    def get_full_name(self, sensor_type: str) -> str:
        return {
            'PIR': 'Passive infrared motion sensor',
            'LDR': 'Light Dependent Resistor',
            'DHT': 'Temperature and humidity sensor',
            'PS': 'Pressure sensor',
        }.get(sensor_type)

    def __str__(self):
        return f'{self.type} : {self.get_full_name(self.type)}'


class Sensor(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=200
    )
    sensor_type = models.ForeignKey(
        SensorType,
        verbose_name=_('sensor type'),
        on_delete=models.CASCADE,
        related_name='sensors'
    )


class Manufacturer(models.Model):
    ...


class Garage(models.Model):
    name = models.CharField(
        verbose_name=_('garage name'),
        max_length=200
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=255,
        blank=True
    )

    class Meta:
        verbose_name = 'Garage'
        verbose_name_plural = 'Garages'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Floor(models.Model):
    name = models.CharField(
        verbose_name=_('floor name'),
        max_length=200
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=255,
        blank=True
    )
    garage = models.ForeignKey(
        Garage,
        on_delete=models.CASCADE,
        related_name='floors'
    )

    class Meta:
        verbose_name = 'Floor'
        verbose_name_plural = 'Floors'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} in № {self.garage.name} garage'


class Room(models.Model):
    name = models.CharField(
        verbose_name='Room',
        max_length=200
    )
    description = models.CharField(
        verbose_name=_('description'),
        max_length=255,
        blank=True
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    sensors = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        verbose_name=_('sensors'),
    )
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
        return f'{self.name}'
