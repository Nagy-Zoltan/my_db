from database.model.db import Database
from database.requests.abstract_request import AbstractRequest


class DropDBByNameRequest(AbstractRequest):

    def __init__(self, name: str):
        self.name = name

    def execute(self, db=None):
        return Database.delete_database(self.name)

    def __repr__(self):
        return f'DropDBByNameRequest(db={self.name})'
