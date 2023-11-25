import socket

from network.consts import INVALID_QUERY, MSG_BUFF_SIZE
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
            msg = self.read_from_socket()
            print(f'Handling request from {self.addr_str}')
            print(f'Request: {msg}')
            request_obj = self._request_parser.get_request_obj(client=self, request_string=msg)
            print(request_obj)
            if request_obj is not None:
                resp = request_obj.execute()
            else:
                resp = INVALID_QUERY
            print(resp)
            self.write_to_socket(resp)

    def read_from_socket(self):
        encoded_msg = self._sock.recv(MSG_BUFF_SIZE)
        return encoded_msg.decode().strip()

    def write_to_socket(self, data: str | bytes):
        if isinstance(data, str):
            msg = data.encode()
        else:
            msg = data
        msg = msg + b'\n'
        self._sock.send(msg)
