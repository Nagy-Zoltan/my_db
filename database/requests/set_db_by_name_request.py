from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_EXIST
from database.model.db import Database


class SetDBByNameRequest(AbstractRequest):

    def __init__(self, client, name: str):
        self.client = client
        self.name = name

    def execute(self):
        try:
            database = Database.name_to_db[self.name]
            self.client.db = database
            return repr(database)
        except KeyError:
            return DB_NOT_EXIST

    def __repr__(self):
        return f'SetDBByNameRequest(client={self.client.addr_str}, name={self.name})'
