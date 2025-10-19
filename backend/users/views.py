from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default CRUD actions, with caching for the list view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to implement caching.
        """
        
        cache_key = "user_list"
        
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print("Serving user list from CACHE")
            return Response(cached_data)
            
        print("Serving user list from DATABASE")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        cache.set(cache_key, data, timeout=900)
        
        return Response(data)