from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Inventory, Item # <-- Import Item
from .serializers import InventorySerializer

class InventoryView(APIView):
    """
    Handles fetching and updating a player's inventory.
    Implements Redis caching for fast read operations.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cache_key = f"inventory_{request.user.id}"
        cached_inventory = cache.get(cache_key)
        if cached_inventory:
            print(f"Serving inventory for user {request.user.username} from CACHE")
            return Response(cached_inventory)
        
        print(f"Serving inventory for user {request.user.username} from DATABASE")
        inventory, _ = Inventory.objects.get_or_create(user=request.user)
        serializer = InventorySerializer(inventory)
        data = serializer.data
        cache.set(cache_key, data, timeout=300)
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        Adds an item to the user's inventory.
        """
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({"error": "item_id is required"}, status=400)

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        inventory, _ = Inventory.objects.get_or_create(user=request.user)
        inventory.items.add(item)
        
        cache_key = f"inventory_{request.user.id}"
        cache.delete(cache_key)
        print(f"CACHE invalidated for user {request.user.username}")

        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=200)