import requests
from .config import get_config


class Queue:
    def __init__(self, session):
        _, _, _, queue_base_url = get_config()
        self.queue_base_url = queue_base_url
        session.authenticate()

    def starting_process(self):
        response = requests.get(f"{self.queue_base_url}/process")
        if response.status_code == 200:
            self.request_id = response.json().get("request_id")
            return True
        return False

    def process_is_done(self):
        response = requests.post(
            f"{self.queue_base_url}/stop", json={"request_id": self.request_id}
        )
        if response.status_code == 200:
            return True
        return False
