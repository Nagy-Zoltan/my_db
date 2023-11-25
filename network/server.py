import socket
import threading
import time

from network.client import Client


class Server:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind((ip, port))
        self._sock.listen()

        self.clients = {}

    def _start(self, max_clients: int = 16):
        print(f'Accepting clients at {self.ip}:{self.port}')
        while True:
            if len(self.clients) >= max_clients:
                time.sleep(1)
                continue
            sock_obj, sock = self._sock.accept()
            print(f'Client connected from {sock[0]}:{sock[1]} ({len(self.clients) + 1} / {max_clients})')
            client = Client(sock=sock_obj, ip=sock[0], port=sock[1])
            self.clients[client.addr_str] = client

            self.serve_client(client=client)

    def start(self):
        threading.Thread(target=self._start, args=()).start()

    @staticmethod
    def _serve_client(client: Client):
        client.get_requests()

    def serve_client(self, client: Client):
        threading.Thread(target=self._serve_client, args=(client,)).start()

    def delete_client(self, client: Client):
        del self.clients[client.addr_str]
