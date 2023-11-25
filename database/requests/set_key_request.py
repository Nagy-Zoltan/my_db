from database.requests.abstract_request import AbstractRequest


class SetKeyRequest(AbstractRequest):

    def __init__(self, db=None, key: str = None, val: dict | int | str = None):
        self.db = db
        self.key = key
        self.val = val

    def execute(self, db=None):
        if self.db is None and db is None:
            raise RuntimeError('Please specify db to set key in.')
        if db is None:
            db = self.db
        else:
            self.db = db
        return db.set_data(key=self.key, val=self.val)

    def __repr__(self):
        return f'SetKeyRequest(db={self.db.name}, key={self.key}, val={self.val})'
