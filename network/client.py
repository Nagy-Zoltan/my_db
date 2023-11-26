import socket

from database.model.consts import DB_NOT_EXIST
from database.model.db import Database
from network.consts import INVALID_QUERY, MSG_BUFF_SIZE
from network.request_parser import RequestParser


class Client:

    _request_parser = RequestParser()
    _server = None

    def __init__(self, sock: socket.socket, ip: str = None, port: int = None):
        self.ip = ip or sock.getpeername()[0]
        self.port = port or sock.getpeername()[1]
        self.addr_str = f'{ip}:{port}'
        self._sock = sock
        self._db_selector = None

    @property
    def db_selector(self):
        return self._db_selector

    @db_selector.setter
    def db_selector(self, db_selector):
        self._db_selector = db_selector

    def get_database(self):
        result = Database.get_database(self._db_selector)
        if result == DB_NOT_EXIST:
            result = None
        return result

    def get_requests(self):
        while True:
            msg = self.read_from_socket()
            if msg is None:
                self._server.delete_client(self)
                return
            self.handle_request(request=msg)

    def handle_request(self, request):
        print(f'Handling request from {self.addr_str}')
        print(f'Request: {request}')
        request_obj = self._request_parser.get_request_obj(client=self, request_string=request)
        print(request_obj)
        if request_obj is not None:
            resp = request_obj.execute()
        else:
            resp = INVALID_QUERY
        resp_str = str(resp)
        print(resp_str)
        self.write_to_socket(resp_str)

    def read_from_socket(self):
        try:
            encoded_msg = self._sock.recv(MSG_BUFF_SIZE)
        except (ConnectionAbortedError, ConnectionResetError):
            return
        if not encoded_msg:
            return
        return encoded_msg.decode().strip()

    def write_to_socket(self, data: str | bytes):
        if isinstance(data, str):
            msg = data.encode()
        else:
            msg = data
        msg = msg + b'\n'
        self._sock.send(msg)

    @classmethod
    def get_server(cls):
        return cls._server

    @classmethod
    def set_server(cls, server):
        cls._server = server
