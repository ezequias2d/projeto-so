import socket
#from asynclib import TaskManager
from message.literalMessage import LiteralMessage
import tokens

from connection import Connection

class MinionConnection(Connection):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)
    
    def send_job(self, imagedata, dstfilename, token, blocking=True):
        self.acquire(blocking)
        
        self.send_literal(token, False)
        self.send_literal(imagedata, False)
        self.send_literal(dstfilename, False)
        
        coreIndex = self.receive_message(False).value
        
        self.release(blocking)
        
        return coreIndex
        
        
        