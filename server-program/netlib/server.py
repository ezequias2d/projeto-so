import socket
import selectors
import types

class Server:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.continueLoop = True
        
    def start(self):
        self.selector = selectors.DefaultSelector()
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        
        print("listening on ", (self.host, self.port))
        self.socket.setblocking(False)
        
        self.selector.register(self.socket, selectors.EVENT_READ, data = None)
    
        self.continueLoop = True
        while self.continueLoop:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)
            
    
    def accept_wrapper(self, socket):
        conn, addr = socket.accept()
        print('Accepted connection from ', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr = addr, inb = b'', outb = b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(conn, events, data=data)
        
    
    def service_connection(self, key, mask):
        pass