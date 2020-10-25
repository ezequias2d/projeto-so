import socket
#from asynclib import TaskManager
from message.literalMessage import LiteralMessage
import tokens

from connection import Connection

class MinionConnection(Connection):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)
        
    def update(self):
        pass
    
    def get_avaliable_cores(self, blocking=True):
        self.acquire(blocking)
        
        message = LiteralMessage(tokens.GET_AVALIABLE_CORES)
        
        self.send_message(message, False)
        result = self.receive_message(False)
        
        self.release(blocking)
        
        return result.value
    
    def do_job(self, job, filename, client_id, blocking=True):
        self.acquire(blocking)
        
        jobMessage = LiteralMessage(job)
        clientIdMessage = LiteralMessage(client_id)
        filenameMessage = LiteralMessage(filename)
        
        self.send_message(jobMessage, False)
        self.send_message(clientIdMessage, False)
        self.send_message(filenameMessage, False)
        
        self.release(blocking)
        
        
        