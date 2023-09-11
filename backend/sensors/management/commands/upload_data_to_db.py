import json
from typing import Dict

from django.core.management.base import BaseCommand
from django.db import models

from garage.settings import BASE_DIR
from sensors.models import Floor, Garage, Manufacturer, Room, Tag, User

MODELS_DATA = {
    User: 'users.json',
    Tag: 'tags.json',
    Manufacturer: 'manufacturer.json',
    Garage: 'garage.json',
    Floor: 'floor.json',
}

DATA_PATH = f'{BASE_DIR}/data/'


class Command(BaseCommand):
    help = 'Import JSON data to database'

    def is_entries_exist(self, model: models.Model) -> bool:
        """Check db entries existing."""
        return True if model.objects.exists() else False

    def statistics_info(self, stat: Dict[str, int]) -> str:
        """Print information about add values."""
        return (
            f'Add new entries: {stat}'
            if any([value for value in stat.values()])
            else ('No entries was add.')
        )

    def handle(self, *args, **options):
        stat: Dict[str, int] = {}

        for model, json_file in MODELS_DATA.items():
            if self.is_entries_exist(model):
                print(
                    f'Database already have entries for '
                    f'`{model._meta.model_name}`: '
                    f'{model.objects.count()} entries.'
                )
                continue

            with open(
                f'{DATA_PATH}/{json_file}', encoding='utf-8', newline=''
            ) as file:
                stat[json_file] = model.objects.count()

                data = json.load(file)

                if model == User:
                    for record in data:
                        model.objects.create_superuser(**record)

                if model in [Tag, Garage, Manufacturer]:
                    model.objects.bulk_create(
                        model(**record) for record in data
                    )

                if model in [Floor, Room]:
                    for record in data:
                        garage = Garage.objects.filter(
                            name__icontains=record.pop('garage')).get()
                        obj = model.objects.create(garage=garage, **record)
                        obj.save()

                stat[json_file] = (model.objects.count() - stat.get(json_file))

        print(self.statistics_info(stat))
