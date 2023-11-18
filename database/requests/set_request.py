from database.requests.abstract_request import AbstractRequest


class SetRequest(AbstractRequest):

    def __init__(self, db, key: str, val: dict | int | str):
        self.db = db
        self.key = key
        self.val = val

    def execute(self):
        return self.db.set_data(key=self.key, val=self.val)
