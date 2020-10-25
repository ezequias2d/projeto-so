import socket
#from asynclib import TaskManager
from connection import Connection

class ClientConnection(Connection):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)
    