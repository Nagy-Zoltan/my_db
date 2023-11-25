from database.requests.abstract_request import AbstractRequest
from database.model.db import Database


class CreateDBRequest(AbstractRequest):

    def __init__(self, name: str):
        self.name = name

    def execute(self):
        return Database(name=self.name)

    def __repr__(self):
        return f'CreateDBRequest(name={self.name})'
