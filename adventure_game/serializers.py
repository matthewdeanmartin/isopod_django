from rest_framework import serializers
from .models import Location, Item, Player

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'description', 'north', 'south', 'east', 'west']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'location']

class PlayerSerializer(serializers.ModelSerializer):
    inventory = ItemSerializer(many=True, read_only=True)
    current_location = LocationSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ['identity', 'current_location', 'inventory']
