import socket
from threading import Lock

class Connection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self._lock = Lock()
        
    def lock(self):
        self._lock.acquire()
        
    def release(self):
        self._lock.release()