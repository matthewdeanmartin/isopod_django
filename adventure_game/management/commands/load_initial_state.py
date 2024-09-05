import toml
from django.core.management.base import BaseCommand
from adventure_game.models import Location, Item


class Command(BaseCommand):
    help = 'Load initial game state from TOML file'

    def handle(self, *args, **kwargs):
        with open('initial_state.toml', encoding="utf-8") as file:
            data = toml.load(file)

        locations = {}
        for loc_name, loc_data in data['locations'].items():
            location = Location.objects.create(
                name=loc_name,
                description=loc_data['description']
            )
            locations[loc_name] = location

        for loc_name, loc_data in data['locations'].items():
            location = locations[loc_name]
            for direction in ['north', 'south', 'east', 'west']:
                if loc_data.get(direction):
                    setattr(location, direction, locations[loc_data[direction]])
            location.save()

        for loc_name, item_name in data['items'].items():
            Item.objects.create(name=item_name, location=locations[loc_name])

        self.stdout.write(self.style.SUCCESS('Initial game state loaded successfully.'))
