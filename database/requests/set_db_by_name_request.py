from database.requests.abstract_request import AbstractRequest
from database.requests.consts import DB_NOT_EXIST
from database.model.db import Database


class SetDBByNameRequest(AbstractRequest):

    def __init__(self, client, name: str):
        self.client = client
        self.name = name

    def execute(self):
        self.client.db_selector = self.name
        result = Database.get_database(self.name)
        return result

    def __repr__(self):
        return f'SetDBByNameRequest(client={self.client.addr_str}, name={self.name})'
