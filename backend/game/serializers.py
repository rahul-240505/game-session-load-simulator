from rest_framework import serializers
from .models import Item, Inventory

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'value']

class InventorySerializer(serializers.ModelSerializer):
    # We want to show the full item details, not just the ID.
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Inventory
        fields = ['user', 'items']
