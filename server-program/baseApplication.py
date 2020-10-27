import socket
import tokens
import connection
import io
import os
from PIL import Image
from message.literalMessage import LiteralMessage

class BaseApplication(connection.Connection):
    
    def __init__(self, host, port, connectionToken):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        super().__init__(sock, '{}:{}'.format(host, port))
        self.send_literal(connectionToken)
        
        result = self.receive_message().value
        
        if result != tokens.SUCESSFUL_CONNECTION:
            raise Exception("The connections failed.")
        else:
            print("Connected successfully with {}:{}.".format(host, port))
            
        self.menu()
        
    def menu(self):
        pass
        
    def get_files_from_storage(self):
        self.send_literal(tokens.GET_NUMBER_OF_FILES)
        number = self.receive_message().value
        
        list = []
        for i in range(0, number):
            self.send_literal(tokens.GET_NAME_OF_FILE)
            self.send_literal(i)
            list.append(self.receive_message().value)
            
        return list
    
    def get_file(self, filename):
        self.send_literal(tokens.GET_FILE)
        self.send_literal(filename)
        return self.receive_message().value
    
    def send_file(self, filename):
        self.send_literal(tokens.SAVE_FILE)
        self.send_literal(os.path.basename(filename))
        
        data = self.readbytes(filename)
        self.send_literal(data)
        
    def readbytes(self, filename):
        
        f = open(filename, 'rb')
        f.seek(0, 2)
        size = f.tell()
        f.seek(0)
        data = f.read(size)
        f.close()
        return data