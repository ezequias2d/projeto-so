import sys
import socket
import connection

class Server:
    # enterClientMethod(connection : Connection)
    _enterClientMethod = None
    # exitClientMethod(connection : Connection)
    _exitClientMethod = None
    
    def __init__(self, enterClientMethod, exitClientMethod, host = '127.0.0.1', port = 65432):
        if not (isinstance(host, str) and isinstance(port, int)) :
            raise ValueError('host or port argument is not in valid types, str, int.')
        
        self._host = host
        self._port = port
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._host, self._port))
            s.listen()
            
            conn, addr = s.accept()
            
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
    
        


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)