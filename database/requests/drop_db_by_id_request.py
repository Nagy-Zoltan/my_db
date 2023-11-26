from database.model.db import Database
from database.requests.abstract_request import AbstractRequest


class DropDBByIDRequest(AbstractRequest):

    def __init__(self, id_: int):
        self.id = id_

    def execute(self):
        return Database.delete_database(self.id)

    def __repr__(self):
        return f'DropDBByIDRequest(id={self.id})'
