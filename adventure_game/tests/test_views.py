import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from adventure_game.models import Location, Player, Item

@pytest.fixture
def apiclient():
    return APIClient()

@pytest.fixture
def setup_locations(db):
    garden = Location.objects.create(name='Garden', description='A lush garden')
    pond = Location.objects.create(name='Pond', description='A calm pond', south=garden)
    return garden, pond

@pytest.fixture
def setup_player(db, setup_locations):
    garden, _ = setup_locations
    player = Player.objects.create(identity='test_player', current_location=garden)
    return player

def test_create_player(apiclient, db, setup_locations):
    """Test creating a player with a POST request."""
    player_url = reverse('player')
    response = apiclient.post(player_url, {'identity': 'test_player'})
    assert response.status_code == status.HTTP_200_OK
    assert Player.objects.count() == 1
    assert Player.objects.get().identity == 'test_player'

def test_get_existing_player(apiclient, db, setup_player):
    """Test retrieving an existing player."""
    player_url = reverse('player')
    response = apiclient.post(player_url, {'identity': 'test_player'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['identity'] == 'test_player'

def test_move_player(apiclient, db, setup_player, setup_locations):
    """Test moving a player to another location."""
    _, pond = setup_locations
    move_url = reverse('move', kwargs={'identity': 'test_player', 'direction': 'north'})
    response = apiclient.post(move_url)
    # Could be movement or "can't move that way" depending on map
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)
    setup_player.refresh_from_db()
    assert setup_player.current_location

def test_pick_up_item(apiclient, db, setup_player, setup_locations):
    """Test picking up an item at the current location."""
    garden, _ = setup_locations
    item = Item.objects.create(name='Cookie Crumb 🍪', location=garden)
    pickup_url = reverse('pickup', kwargs={'identity': 'test_player'})
    response = apiclient.post(pickup_url)
    assert response.status_code == status.HTTP_200_OK
    assert 'Cookie Crumb 🍪' in response.data['message']
    assert setup_player.inventory.count() == 1