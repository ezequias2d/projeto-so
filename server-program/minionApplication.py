import socket
import tokens
import connection

from message.literalMessage import LiteralMessage

class MinionApplication(connection.Connection):
    
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        super().__init__(sock, '{}:{}'.format(host, port))
        
        
        self.send_literal(tokens.MINION_TOKEN)
        
        while(True):
            message = self.receive_message()
            
            if message.value == tokens.JOB_FLIP_HORIZONTAL:
                pass
                
            
    
    def send_literal(self, value):
        literalMessage = LiteralMessage(value)
        self.send_message(literalMessage.get_bytes())
        

MinionApplication('127.0.0.1', 50007)