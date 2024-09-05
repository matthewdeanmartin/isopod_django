from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    north = models.ForeignKey('self', null=True, blank=True, related_name='north_to', on_delete=models.SET_NULL)
    south = models.ForeignKey('self', null=True, blank=True, related_name='south_to', on_delete=models.SET_NULL)
    east = models.ForeignKey('self', null=True, blank=True, related_name='east_to', on_delete=models.SET_NULL)
    west = models.ForeignKey('self', null=True, blank=True, related_name='west_to', on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Player(models.Model):
    identity = models.CharField(max_length=100, unique=True)  # Self-asserted identity
    current_location = models.ForeignKey(Location, related_name='players', on_delete=models.CASCADE)
    inventory = models.ManyToManyField(Item, related_name='owned_by')

    def has_won(self):
        win_conditions = set(["A Place to Hide 🛏️", "Cookie Crumb 🍪", "Isopod Friend 🐾"])
        inventory_items = set(item.name for item in self.inventory.all())
        return win_conditions.issubset(inventory_items)
