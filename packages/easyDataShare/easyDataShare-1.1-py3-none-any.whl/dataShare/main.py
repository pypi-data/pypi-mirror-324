import socket
import json


class easyDataShare:
    def __init__(self):
        pass

    def connect(self, port, mode: bool, ip='127.0.0.1'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if mode == False:
            self.sock.bind((ip, port))
        self.UDP_IP = ip
        self.UDP_PORT = port

    def write(self, data: list):
        serialized_array = json.dumps(data)
        self.sock.sendto(serialized_array.encode(), (self.UDP_IP, self.UDP_PORT))

    def read(self, buffer_size=1024):
        data, addr = self.sock.recvfrom(buffer_size)
        received_array = json.loads(data.decode())
        return received_array