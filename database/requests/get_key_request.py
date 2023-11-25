from database.requests.abstract_request import AbstractRequest


class GetKeyRequest(AbstractRequest):

    def __init__(self, db=None, key: str = None):
        self.db = db
        self.key = key

    def execute(self, db=None):
        if self.db is None and db is None:
            raise RuntimeError('Please specify db to get key from.')
        if db is None:
            db = self.db
        else:
            self.db = db
        return db.get_data(key=self.key)

    def __repr__(self):
        return f'GetKeyRequest(db={self.db.name}, key={self.key})'
