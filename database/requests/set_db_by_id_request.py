from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_EXIST
from database.model.db import Database


class SetDBByIDRequest(AbstractRequest):

    def __init__(self, client, id_: int):
        self.client = client
        self.id = id_

    def execute(self):
        try:
            database = Database.id_to_db[self.id]
            self.client.db = database
        except KeyError:
            return DB_NOT_EXIST

    def __repr__(self):
        return f'SetDBByIDRequest(client={self.client.addr_str}, id={self.id})'
