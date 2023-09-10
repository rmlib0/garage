# Generated by Django 4.2.4 on 2023-09-10 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='floor name')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='FloorInGarage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Room')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PIR', 'Passive infrared motion sensor'), ('LDR', 'Light Dependent Resistor'), ('DHT', 'Temperature and humidity sensor'), ('PS', 'Pressure sensor')], max_length=300)),
            ],
            options={
                'verbose_name': 'Sensor type',
                'verbose_name_plural': 'Sensor types',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='tag')),
                ('color', models.CharField(max_length=7, unique=True, verbose_name='color')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SensorInRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='sensors.room', verbose_name='Room')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_amount', to='sensors.sensor', verbose_name='Sensor')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensors', to='sensors.sensortype', verbose_name='sensor type'),
        ),
        migrations.AddField(
            model_name='room',
            name='sensors',
            field=models.ManyToManyField(through='sensors.SensorInRoom', to='sensors.sensor', verbose_name='sensors'),
        ),
        migrations.AddField(
            model_name='room',
            name='tags',
            field=models.ManyToManyField(related_name='rooms', to='sensors.tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='garage name')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('floor', models.ManyToManyField(related_name='garage_floor', to='sensors.floor', verbose_name='sensor type')),
            ],
        ),
    ]
