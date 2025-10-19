from django.db import models
from users.models import User

class Item(models.Model):
    """Represents a single item that can exist in the game."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    value = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    """Represents a player's inventory."""
    # Create a one-to-one link to our User model. Each user gets one inventory.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # A list of items the user possesses.
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Inventory"
