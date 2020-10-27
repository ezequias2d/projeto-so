import socket
import tokens
import connection
import io
import os
from PIL import Image
from message.literalMessage import LiteralMessage
from baseApplication import BaseApplication
import asynclib
from asynclib.taskManager import *

class MinionApplication(BaseApplication):
    
    def __init__(self, host, port):        
        super().__init__(host, port, tokens.MINION_TOKEN)
        self.pool = TaskManager('minion_{}_{}_thread_'.format(host, port))
        
        self.loop()
        self.pool.join()
        
    def loop(self):
        while not self.is_closed():
            message = self.receive_message(True, 1.0)
            if message is not None:
                message = message.value
                if self.decode_job(message):
                    pass
                else:
                    print("The job is not valid, {}".format(message))
    
    def decode_job(self, message):        
        action = None
        if message == tokens.JOB_FLIP_HORIZONTAL:
            action = Image.FLIP_LEFT_RIGHT

        elif message == tokens.JOB_FLIP_VERTICAL:
            action = Image.FLIP_TOP_BOTTOM
            
        elif message == tokens.JOB_ROTATE_90:
            action = Image.ROTATE_90
            
        elif message == tokens.JOB_ROTATE_180:
            action = Image.ROTATE_180
            
        elif message == tokens.JOB_ROTATE_270:
            action = Image.ROTATE_270
        else:
             return False
         
        imagedata = self.receive_message().value
        dstfilename = self.receive_message().value
            
        task = self.pool.run(self.job_thread, args = (imagedata, dstfilename, action))
        self.send_literal(task.index)
        
        return True
    
    def job_thread(self, imagedata, dstfilename, action):
        img = self.load_image(imagedata)
        format = img.format
        
        img = img.transpose(action)
        self.save_image(img, dstfilename,format)
    
    def load_image(self, imagedata):
        return Image.open(io.BytesIO(imagedata))
    
    def save_image(self, image, filename, format):
        bytes = io.BytesIO()
        image.save(bytes, format)
        bytes = bytes.getvalue()
        
        self.send_literal(tokens.SAVE_FILE)
        self.send_literal(os.path.basename(filename))
        self.send_literal(bytes)
        
        
host = input('Host: ')
MinionApplication(host, 50007)