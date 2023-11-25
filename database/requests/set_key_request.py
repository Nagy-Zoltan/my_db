from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_SET


class SetKeyRequest(AbstractRequest):

    def __init__(self, db=None, key: str = None, val: dict | int | str = None):
        self.db = db
        self.key = key
        self.val = val

    def execute(self, db=None):
        if self.db is None and db is None:
            return DB_NOT_SET
        if db is None:
            db = self.db
        else:
            self.db = db
        return db.set_data(key=self.key, val=self.val)

    def __repr__(self):
        if self.db is not None:
            return f'SetKeyRequest(db={self.db.name}, key={self.key}, val={self.val})'
        else:
            return f'SetKeyRequest(db={None}, key={self.key}, val={self.val})'
