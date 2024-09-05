from django.urls import path
from .views import PlayerView, MoveView, PickUpItemView, InventoryView



urlpatterns = [
    path('player', PlayerView.as_view(), name='player'),  # This is the player endpoint
    path('player/', PlayerView.as_view(), name='player'),  # This is the player endpoint
    path('player/<str:identity>/', PlayerView.as_view(), name='player'),
    path('move/<str:identity>/<str:direction>/', MoveView.as_view(), name='move'),
    path('pickup/<str:identity>/', PickUpItemView.as_view(), name='pickup'),
    path('inventory/<str:identity>/', InventoryView.as_view(), name='inventory'),
]

