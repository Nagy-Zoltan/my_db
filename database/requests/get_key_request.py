from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_SET


class GetKeyRequest(AbstractRequest):

    def __init__(self, db=None, key: str = None):
        self.db = db
        self.key = key

    def execute(self, db=None):
        if self.db is None and db is None:
            return DB_NOT_SET
        if db is None:
            db = self.db
        else:
            self.db = db
        return str(db.get_data(key=self.key))

    def __repr__(self):
        if self.db is not None:
            return f'GetKeyRequest(db={self.db.name}, key={self.key})'
        else:
            return f'GetKeyRequest(db={None}, key={self.key})'
