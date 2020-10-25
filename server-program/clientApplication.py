import socket
import tokens
from message.literalMessage import LiteralMessage

class ClientApplication:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.send_literal(tokens.CLIENT_TOKEN)
        
    
    def send_literal(self, value):
        literalMessage = LiteralMessage(value)
        self.sock.send(literalMessage)
        

ClientApplication('localhost', 50007)