import pytest
from adventure_game.models import Location, Player, Item

@pytest.mark.django_db
class TestLocationModel:

    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.garden = Location.objects.create(name='Garden', description='A lush garden')
        self.pond = Location.objects.create(name='Pond', description='A calm pond', south=self.garden)

    def test_location_creation(self):
        """Test that locations are created properly."""
        assert self.garden.name == 'Garden'
        assert self.pond.south == self.garden

    def test_location_navigation(self):
        """Test that locations are connected correctly."""
        assert self.pond.south.name == 'Garden'


@pytest.mark.django_db
class TestPlayerModel:

    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.location = Location.objects.create(name='Garden', description='A lush garden')
        self.player = Player.objects.create(identity='test_player', current_location=self.location)

    def test_player_creation(self):
        """Test that a player is created with the correct initial location."""
        assert self.player.identity == 'test_player'
        assert self.player.current_location == self.location

    def test_inventory(self):
        """Test that player inventory starts empty and can add items."""
        item = Item.objects.create(name='Cookie Crumb 🍪', location=self.location)
        assert self.player.inventory.count() == 0
        self.player.inventory.add(item)
        assert self.player.inventory.count() == 1
        assert self.player.inventory.first().name == 'Cookie Crumb 🍪'