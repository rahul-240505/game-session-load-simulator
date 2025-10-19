from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from .models import Inventory
from .serializers import InventorySerializer

class InventoryView(APIView):
    """
    Handles fetching and updating a player's inventory.
    Implements Redis caching for fast read operations.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Define a unique cache key for the currently logged-in user
        cache_key = f"inventory_{request.user.id}"
        
        cached_inventory = cache.get(cache_key)
        
        if cached_inventory:
            print(f"Serving inventory for user {request.user.username} from CACHE")
            return Response(cached_inventory)
        
        print(f"Serving inventory for user {request.user.username} from DATABASE")
        inventory, created = Inventory.objects.get_or_create(user=request.user)
        serializer = InventorySerializer(inventory)
        data = serializer.data
        
        cache.set(cache_key, data, timeout=300)
        
        return Response(data)

