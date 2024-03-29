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
            
    def remove_file(self):
        filename = input("Filename:")
        self.send_literal(tokens.REMOVE_FILE)
        self.send_literal(filename)
        result = self.receive_message(True, 1.0)
        if result is not None:
            if result.value == tokens.ERROR_MESSAGE or result.value == tokens.INFO_MESSAGE:
                message = self.receive_message().value
                print(message)
        
    def see_a_logfile(self):
        files = [logfile for logfile in self.get_files_from_storage() if os.path.splitext(logfile)[1].lower() == '.log']
        count = 0
        for logfile in files:
            print('{} - {}'.format(count, logfile))
            count += 1
        
        index = int(input('Index:'))
        filename = files[index]
        
        file = self.get_file(filename)
        file = io.BytesIO(file).read()
        
        print('Log:')
        print(file.decode('UTF-8'))
        
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
        print('9 - Remove File from Storage.')
        print('10 - See a logfile.')
        
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
            elif cmd == 9:
                self.remove_file()
            elif cmd == 10:
                self.see_a_logfile()

host = input('Host: ')
ClientApplication(host, 50007)