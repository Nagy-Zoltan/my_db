from database.requests.abstract_request import AbstractRequest


class GetRequest(AbstractRequest):

    def __init__(self, db, key: str):
        self.db = db
        self.key = key

    def execute(self):
        return self.db.get_data(key=self.key)
