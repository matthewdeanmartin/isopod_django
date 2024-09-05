
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Location, Player
from .serializers import ItemSerializer, PlayerSerializer

class PlayerView(APIView):
    def get(self, request, identity):
        player = get_object_or_404(Player, identity=identity)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    # def post(self, request):
    #     identity = request.data.get('identity')
    #     start_location = Location.objects.get(name="Garden")
    #     player, created = Player.objects.get_or_create(identity=identity, defaults={'current_location': start_location})
    #     if created:
    #         player.inventory.clear()
    #     serializer = PlayerSerializer(player)
    #     return Response(serializer.data)


    def post(self, request):
        identity = request.data.get('identity')  # Retrieve identity from request data
        if not identity:
            return Response({"error": "Identity is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the player already exists or create a new one
        start_location = Location.objects.get(name="Garden")  # Ensure the start location exists
        player, created = Player.objects.get_or_create(identity=identity, defaults={'current_location': start_location})

        if created:
            # If a new player is created, ensure the inventory is cleared (or initialized)
            player.inventory.clear()

        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MoveView(APIView):
    def post(self, request, identity, direction):
        print(identity, direction)
        player = get_object_or_404(Player, identity=identity)
        current_location = player.current_location
        next_location = getattr(current_location, direction, None)
        if next_location:
            player.current_location = next_location
            player.save()
            return Response({'message': f'Moved to {next_location.name}'})
        return Response({'message': 'You cannot move in that direction!'}, status=status.HTTP_400_BAD_REQUEST)

class PickUpItemView(APIView):
    def post(self, request, identity):
        player = get_object_or_404(Player, identity=identity)
        current_location = player.current_location
        item = current_location.items.first()  # Assuming only one item per location
        if item:
            player.inventory.add(item)
            player.save()
            if player.has_won():
                return Response({'message': "Congratulations! You've found all three things and won the game! 🎉"})
            return Response({'message': f'Picked up {item.name}'})
        return Response({'message': 'No items to pick up here!'}, status=status.HTTP_400_BAD_REQUEST)

class InventoryView(APIView):
    def get(self, request, identity):
        player = get_object_or_404(Player, identity=identity)
        inventory = player.inventory.all()
        serializer = ItemSerializer(inventory, many=True)
        return Response(serializer.data)
