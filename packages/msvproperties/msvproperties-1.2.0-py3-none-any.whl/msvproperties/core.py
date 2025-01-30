import json
from .config import get_config
from .queue import Queue
from .process import ProcessLogic


class Lead:
    def __init__(self, session):
        _, base_url, _, _ = get_config()
        self.base_url = base_url
        self.auth_session = session
        session.authenticate()

    def insert(self, data):
        url = f"{self.base_url}/api/leads/"
        queue = Queue(self.auth_session)
        queue.starting_process()
        ProcessLogic(data, self.auth_session).start()
        queue.process_is_done()
        response = self.auth_session.make_authenticated_request(
            url, method="POST", data=json.dumps(data.model_dump())
        )
        print(response)
