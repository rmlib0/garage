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
    type = models.Choices()


class SensorInRoom(models.Model):
    ...


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
    ...


class FloorInGarage(models.Model):
    ...


class Room(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Room',
        max_length=200
    )
    sensors = models.ManyToManyField(
        Sensor,
        through='SensorInRoom',
        verbose_name=_('sensors'),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'
