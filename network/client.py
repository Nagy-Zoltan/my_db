import socket

from network.consts import MSG_BUFF_SIZE
from network.request_parser import RequestParser


class Client:

    _request_parser = RequestParser()

    def __init__(self, sock: socket.socket, ip: str = None, port: int = None):
        self.ip = ip or sock.getpeername()[0]
        self.port = port or sock.getpeername()[1]
        self.addr_str = f'{ip}:{port}'
        self._sock = sock
        self._db = None

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, database):
        self._db = database

    def get_requests(self):
        while True:
            encoded_msg = self._sock.recv(MSG_BUFF_SIZE)
            msg = encoded_msg.decode().strip()
            print(f'Handling request from {self.ip}:{self.port}')
            print(f'Request: {msg}')
            request_obj = self._request_parser.get_request_obj(client=self, request_string=msg)
            print(request_obj)
            if request_obj is not None:
                request_obj.execute()
            if self._db is not None:
                print(self._db.data)
