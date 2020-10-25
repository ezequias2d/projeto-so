import socket
import tokens
from message.literalMessage import LiteralMessage

class ClientApplication:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.send_literal(tokens.CLIENT_TOKEN)
        
    def print_commands(self):
        print('Commands:')
        print('0 - Exit')
        print('1 - Flip Image Horizontal')
        print('2 - Flip Image Vertical')
        print('3 - Rotate Image 90.')
        print('4 - Rotate Image 180.')
        print('5 - Rotate Image 270.')
        print('6 - See Files in Storage.')
        print('7 - Send File to Storage.')
        print('8 - Get File from Storage.')
        
    def send_literal(self, value):
        literalMessage = LiteralMessage(value)
        self.sock.send(literalMessage.get_bytes())
        

ClientApplication('127.0.0.1', 50007)