import random
import time
from locust import HttpUser, task, between, events
from prometheus_client import start_http_server, Counter, Gauge, Summary

# --- 1. DEFINE OUR CUSTOM METRICS ---
# These will appear in Grafana with these names
REQUEST_COUNT = Counter("game_requests_total", "Total requests made", ["method", "name"])
FAILURE_COUNT = Counter("game_failures_total", "Total failed requests", ["method", "name"])
RESPONSE_TIME = Summary("game_response_time_ms", "Response time in milliseconds", ["method", "name"])
USER_COUNT = Gauge("game_user_count", "Current number of users")

# --- 2. START THE EXPORTER SERVER ---
start_http_server(port=8090, addr="0.0.0.0")

# --- 3. CREATE HOOKS TO UPDATE METRICS ---
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """
    This function is called for every single request Locust makes.
    """
    REQUEST_COUNT.labels(method=request_type, name=name).inc()
    RESPONSE_TIME.labels(method=request_type, name=name).observe(response_time)
    if exception:
        FAILURE_COUNT.labels(method=request_type, name=name).inc()

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    USER_COUNT.set(0)

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    USER_COUNT.set(0)
    
@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    USER_COUNT.set(user_count)


# --- 4. USER CLASS ---
class GameUser(HttpUser):
    wait_time = between(1, 3)
    token = None
    item_ids = []

    def on_start(self):
        random_int = random.randint(1, 100000)
        self.username = f"testuser_{random_int}"
        self.email = f"test_{random_int}@example.com"
        self.password = "SecurePassword123"
        
        self.client.post("/api/users/", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        }, name="/api/users/ [Register]")
        
        response = self.client.post("/api/login/", json={
            "username": self.email,
            "password": self.password
        }, name="/api/login/")
        
        if response.status_code == 200:
            self.token = response.json().get("token")
        
        self.item_ids = [1, 2, 3, 4]

    @task(2) 
    def get_inventory(self):
        if self.token:
            headers = {"Authorization": f"Token {self.token}"}
            self.client.get("/api/game/inventory/", headers=headers, name="/api/game/inventory/ [GET]")

    @task(1) 
    def add_item_to_inventory(self):
        if self.token and self.item_ids:
            headers = {"Authorization": f"Token {self.token}"}
            random_item_id = random.choice(self.item_ids)
            self.client.post(
                "/api/game/inventory/", 
                headers=headers, 
                json={"item_id": random_item_id},
                name="/api/game/inventory/ [POST]"
            )