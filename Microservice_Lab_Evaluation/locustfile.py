from locust import HttpUser, task, constant

class AppUser(HttpUser):
    wait_time = constant(0)   # no waiting, so users = concurrent requests

    @task
    def create_order(self):
        self.client.post("/orders", json={"product_id": 1, "quantity": 2})