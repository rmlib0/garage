# Generated by Django 4.2.4 on 2023-09-10 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0002_remove_garage_floor_floor_garage_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FloorInGarage',
        ),
        migrations.RemoveField(
            model_name='room',
            name='owner',
        ),
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.CharField(blank=True, max_length=255, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='room',
            name='floor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='sensors.floor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='floor',
            name='garage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floors', to='sensors.garage'),
        ),
        migrations.AlterField(
            model_name='garage',
            name='description',
            field=models.CharField(blank=True, max_length=255, verbose_name='description'),
        ),
        migrations.RemoveField(
            model_name='room',
            name='sensors',
        ),
        migrations.AlterField(
            model_name='room',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='sensors.tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='SensorInRoom',
        ),
        migrations.AddField(
            model_name='room',
            name='sensors',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sensors.sensor', verbose_name='sensors'),
            preserve_default=False,
        ),
    ]
