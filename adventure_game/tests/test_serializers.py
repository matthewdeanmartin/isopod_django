import pytest
from adventure_game.models import Location, Item
from adventure_game.serializers import LocationSerializer, ItemSerializer

@pytest.fixture
def setup_location(db):
    return Location.objects.create(name='Garden', description='A lush garden')

@pytest.fixture
def setup_item(db, setup_location):
    return Item.objects.create(name='Cookie Crumb 🍪', location=setup_location)

def test_location_serialization(setup_location):
    """Test that location serialization works as expected."""
    serializer = LocationSerializer(setup_location)
    assert serializer.data['name'] == 'Garden'
    assert serializer.data['description'] == 'A lush garden'

def test_item_serialization(setup_item, setup_location):
    """Test that item serialization works as expected."""
    serializer = ItemSerializer(setup_item)
    assert serializer.data['name'] == 'Cookie Crumb 🍪'
    assert serializer.data['location'] == setup_location.id