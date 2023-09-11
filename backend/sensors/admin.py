from django.contrib import admin

from .models import (DHT, PIR, PR, Floor, Garage, Manufacturer, Room, Sensor,
                     Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(DHT)
class DHTAdmin(admin.ModelAdmin):
    pass


@admin.register(PIR)
class PIRAdmin(admin.ModelAdmin):
    pass


@admin.register(PR)
class PRAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    pass


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
