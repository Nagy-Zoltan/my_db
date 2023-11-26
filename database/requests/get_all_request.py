from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_SET


class GetAllRequest(AbstractRequest):

    def __init__(self, db=None):
        self.db = db

    def execute(self, db=None):
        if self.db is None and db is None:
            return DB_NOT_SET
        if db is None:
            db = self.db
        else:
            self.db = db
        return db.get_all()

    def __repr__(self):
        if self.db is not None:
            return f'GetAllRequest(db={self.db.name})'
        else:
            return f'GetAllRequest(db={None})'
