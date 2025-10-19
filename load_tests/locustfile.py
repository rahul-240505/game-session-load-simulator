import random
from locust import HttpUser, task, between

class GameUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    item_ids = []

    def on_start(self):
        """
        Called when a Locust user starts. Handles registration, login,
        and fetching the list of available items.
        """
        random_int = random.randint(1, 100000)
        self.username = f"testuser_{random_int}"
        self.email = f"test_{random_int}@example.com"
        self.password = "SecurePassword123"
        
        self.client.post("/api/users/", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        
        response = self.client.post("/api/login/", json={
            "username": self.email,
            "password": self.password
        })
        
        if response.status_code == 200:
            self.token = response.json().get("token")
        
        self.item_ids = [1, 2, 3, 4]

    @task(2)
    def get_inventory(self):
        """Simulates fetching the inventory (a READ operation)."""
        if self.token:
            headers = {"Authorization": f"Token {self.token}"}
            self.client.get("/api/game/inventory/", headers=headers, name="/api/game/inventory/ [GET]")

    @task(1)
    def add_item_to_inventory(self):
        """Simulates adding an item to the inventory (a WRITE operation)."""
        if self.token and self.item_ids:
            headers = {"Authorization": f"Token {self.token}"}
            random_item_id = random.choice(self.item_ids)
            self.client.post(
                "/api/game/inventory/", 
                headers=headers, 
                json={"item_id": random_item_id},
                name="/api/game/inventory/ [POST]"
            )