import random
from locust import HttpUser, task, between

class GameUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Called when a Locust user starts. This is where we will handle
        the registration and login logic to get an auth token.
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
        
        self.token = response.json()["token"]
        
    @task
    def get_all_users(self):
        """
        This is the main task the user will perform repeatedly after logging in.
        It simulates an authenticated API call.
        """
        headers = {"Authorization": f"Token {self.token}"}
        self.client.get("/api/users/", headers=headers, name="/api/users/ (Authenticated)")