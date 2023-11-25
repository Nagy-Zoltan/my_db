from database.model.db import Database
from database.requests.get_key_request import GetKeyRequest
from database.requests.set_key_request import SetKeyRequest
from network.server import Server


server = Server('localhost', 1234)


server.accept()
