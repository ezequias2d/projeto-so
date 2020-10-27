import socket
import tokens
import connection
import io
import os
from PIL import Image
from message.literalMessage import LiteralMessage
from baseApplication import BaseApplication

class ClientApplication(BaseApplication):
    
    def __init__(self, host, port):
        super().__init__(host, port, tokens.CLIENT_TOKEN)
    
    def show_image_file_from_storage(self):
        filename = input("Filename:")
        file = self.get_file(filename)
        img = Image.open(io.BytesIO(file))
        img.show()   
    
    def see_files_in_storage(self):        
        files = self.get_files_from_storage()
        for filename in files:
            print(filename)
    
    def send_file_to_storage(self):
        filename = input("Filename:")
        self.send_file(filename)
        
    def send_job(self, token):
        filename = input("Filename:")
        dstfilename = input("Destination filename:")
        self.send_literal(token)
        self.send_literal(filename)
        self.send_literal(dstfilename)
        
        messageToken = self.receive_message().value
        message = self.receive_message().value
        
        if messageToken == tokens.INFO_MESSAGE or messageToken == tokens.ERROR_MESSAGE:
            print(message)
        
        
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
        print('8 - Show Image File from Storage.')
        
    def menu(self):
        while not self.is_closed():
            self.print_commands()
            cmd = int(input("Cmd>"))
            if cmd == 0:
                self.close()
            elif cmd == 1:
                self.send_job(tokens.JOB_FLIP_HORIZONTAL)
            elif cmd == 2:
                self.send_job(tokens.JOB_FLIP_VERTICAL)
            elif cmd == 3:
                self.send_job(tokens.JOB_ROTATE_90)
            elif cmd == 4:
                self.send_job(tokens.JOB_ROTATE_180)
            elif cmd == 5:
                self.send_job(tokens.JOB_ROTATE_270)
            elif cmd == 6:
                self.see_files_in_storage()
            elif cmd == 7:
                self.send_file_to_storage()
            elif cmd == 8:
                self.show_image_file_from_storage()

host = input('Host: ')
ClientApplication(host, 50007)