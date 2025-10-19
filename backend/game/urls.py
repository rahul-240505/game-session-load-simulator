from django.urls import path
from .views import InventoryView

urlpatterns = [
    path('inventory/', InventoryView.as_view(), name='player_inventory'),
]