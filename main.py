from network.client import Client
from network.server import Server


server = Server('localhost', 1234)
Client.set_server(server)

server.start()
