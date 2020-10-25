import socket
import types
import logging
import threading
import tokens

import asynclib
from asynclib.taskManager import *


from collections import deque

from clientConnection import ClientConnection
from minionConnection import MinionConnection
from message.literalMessage import LiteralMessage
from message.objectMessage import ObjectMessage



class Server:
    
    def __init__(self, port=50007):
        """Initialize the server object.

        Args:
            port (int): Port.
        """
        #socket.gethostbyname(socket.gethostname())
        self.host = 'localhost'
        self.port = port
        self.taskManager = TaskManager('server_thread_')
        
        self.minions = deque()
        self.minions_lock = threading.Lock()
        
        self.clients = deque()
        self.clients_lock = threading.Lock()
        
    def start(self):
        """Starts the server process.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        
        logging.info("listening on {}:{}".format(self.host, self.port))
        print("listening on ", (self.host, self.port))
        
        listeningThread = threading.Thread(target=self.newConnectionTask, name='server_lister_thread')
        listeningThread.start()
        
        minionsThread = threading.Thread(target=self.minions_thread, name='minions_thread')
        minionsThread.start()
        
        clientThread = threading.Thread(target=self.clients_thread, name='clients_thread')
        clientThread.start()
        
        listeningThread.join()
        minionsThread.join()
        clientThread.join()
        
                
    def newConnectionTask(self):
        self.continueListening = True
        while self.continueListening:
            conn, addr = self.socket.accept()
            
            logging.info("connected to {}:{}".format(addr[0], addr[1]))
            print("connected to {}:{}".format(addr[0], addr[1]))
            
            messageData = conn.recv(1024)
            message = LiteralMessage.from_bytes(messageData)
                       
            if message.value == tokens.MINION_TOKEN:
                
                self.minions_lock.acquire()
                self.minions.append(MinionConnection(conn, addr))
                self.minions_lock.release()
                
            elif message.value == tokens.CLIENT_TOKEN:
                
                self.clients_lock.acquire()
                self.clients.append(ClientConnection(conn, addr))
                self.clients_lock.acquire()
    
    def minions_thread(self):
        self.continueMinions = True
        
        while(self.continueMinions):
            
            self.minions_lock.acquire()
            try:
                minion = self.minions.popleft()
            except IndexError:
                continue
        
            response = minion.update()
            
            if not response is None:
                # check if have a reponse
                
                # acquire the client lock.
                self.clients_lock.acquire()
                addressedClient = None
                
                # search by client address
                for client in self.clients:
                    if client.addr == response.addressDestination:
                        addressedClient = client
                        break
                
                # if has client, send the response to the client.
                if not addressedClient is None:
                    message = ObjectMessage(response, 'miRs')
                    client.send_message(message)
                
                #release the client lock.
                self.clients_lock.release()
        
            self.minions.append(minion)
            self.minions_lock.release()
        
        self.minions_lock.acquire()
        
        for connection in self.minions:
            connection.close()
            
        self.minions_lock.release()
    
    def clients_thread(self):
        self.continueClients = True
        
        while(self.continueClients):
            
            self.clients_lock.acquire()
        
            try:
                client = self.clients.popleft()
            except IndexError:
                continue
        
            client.update()
        
            self.clients.append(client)
        
            self.clients_lock.release()
        
        self.clients_lock.acquire()
        
        for connection in self.clients:
            connection.close()
            
        self.clients_lock.release()