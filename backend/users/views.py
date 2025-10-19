from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer
#import time (For perfomeance testing simulation)

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    """ 
    Uncomment the below method to simulate a slow database query for performance testing.
    """
    # def list(self, request, *args, **kwargs):
    #     print("Simulating a slow database query...")
    #     time.sleep(1)
    #     return super().list(request, *args, **kwargs)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
