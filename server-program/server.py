import socket
import types
import logging
import threading
import tokens
import random

from storage import Storage
from collections import deque

from connection import Connection
from clientConnection import ClientConnection
from minionConnection import MinionConnection
from message.literalMessage import LiteralMessage

MSG_SIZE = 1024

class Server:
    
    def __init__(self, host, port=50007):
        """Initialize the server object.

        Args:
            port (int): Port.
        """
        self.host = host
        self.port = port
        self.storage = Storage()
        
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
            
            connection = Connection(conn, addr)
            message = connection.receive_message()
            connection.send_message(LiteralMessage(tokens.SUCESSFUL_CONNECTION))
            connection = None
            
            outputLog = "connected to {}:{} as a ".format(addr[0], addr[1])
            
            if message.value == tokens.MINION_TOKEN:
                
                self.minions_lock.acquire()
                self.minions.append(MinionConnection(conn, addr))
                self.minions_lock.release()
                outputLog += "minion"
            elif message.value == tokens.CLIENT_TOKEN:
                self.clients_lock.acquire()
                self.clients.append(ClientConnection(conn, addr))
                self.clients_lock.release()
                outputLog += "client"
            else:
                outputLog += "undefined"

            logging.info(outputLog)
            print(outputLog)
    
    def minions_thread(self):
        self.continueMinions = True
        
        while(self.continueMinions):
            
            self.minions_lock.acquire()
        
            try:
                minion = self.minions.popleft()
            except IndexError:
                self.minions_lock.release()
                continue
        
            try:
                message = minion.receive_message(True, 1.0)
            except Exception as e:
                print(e)
                logging.info(e)
                self.clients_lock.release()
                continue
            
            if message is not None:
                message = message.value
                if self.try_decode_storages(minion, message):
                    pass
                else:
                    print("Unknown message of value '{}', sended by the minion '{}'".format(message, minion.get_addr()))
                
            if not minion.is_closed():
                self.minions.append(minion)
            else:
                print('')
        
            self.minions_lock.release()
    
    def clients_thread(self):
        self.continueClients = True
        
        while(self.continueClients):
            
            self.clients_lock.acquire()
        
            try:
                client = self.clients.popleft()
            except IndexError:
                self.clients_lock.release()
                continue
            
            try:
                message = client.receive_message().value
            except Exception as e:
                message = "client '{}':{}".format(client.get_addr(), e)
                print(message)
                logging.info(message)
                self.clients_lock.release()
                continue
            
            if self.try_decode_storages(client, message):
                pass
            elif self.try_decode_client_job(client, message):
                pass
            else:
                print("Unknown message of value '{}', sended by the client '{}'".format(message, client.get_addr()))
            
                
            if not client.is_closed():
                self.clients.append(client)
        
            self.clients_lock.release()
        
        # close connections with clients
        self.clients_lock.acquire()
        
        for connection in self.clients:
            connection.close()
            
        self.clients_lock.release()
        
        
    def try_decode_storages(self, connection, token):
        try:
            if token == tokens.GET_FILE_SIZE:
                filename = connection.receive_message().value
                size = self.storage.get_file_size(filename)
            
                connection.send_message(LiteralMessage(size))
            elif token == tokens.IS_FILE:
                filename = connection.receive_message().value
                result = self.storage.is_file(filename)
                connection.send_message(LiteralMessage(result))
            
            elif token == tokens.GET_NUMBER_OF_FILES:
                number = self.storage.get_number_of_files()
                connection.send_message(LiteralMessage(number))
            
            elif token == tokens.GET_NAME_OF_FILE:
                index = connection.receive_message().value
                name = self.storage.get_name_of_file(index)
                connection.send_message(LiteralMessage(name))
            
            elif token == tokens.SAVE_FILE:
                filename = connection.receive_message().value
                data = connection.receive_message().value
                self.storage.save_file(filename, data)
            
            elif token == tokens.REMOVE_FILE:
                filename = connection.receive_message().value
                self.storage.remove_file(filename)
            elif token == tokens.GET_FILE:
                filename = connection.receive_message().value
                data = self.storage.get_file(filename)
                connection.send_message(LiteralMessage(data))
            else:
                return False
        except BaseException as e:
            connection.send_literal(tokens.ERROR_MESSAGE)
            errorMessage = "The storege operation from '{}' resulted in a exception: {}".format(connection.get_addr(), e)
            connection.send_literal(errorMessage)
            logging.error(errorMessage)
            print(errorMessage)
            
        return True
    
    def try_decode_client_job(self, connection, token):
        filename = None
        dstfilename = None
        if (token == tokens.JOB_FLIP_HORIZONTAL or
            token == tokens.JOB_FLIP_VERTICAL   or
            token == tokens.JOB_ROTATE_90       or
            token == tokens.JOB_ROTATE_180      or
            token == tokens.JOB_ROTATE_270):
            
            filename = connection.receive_message().value
            dstfilename = connection.receive_message().value
        else:
            return False
        
        if not self.storage.is_file(filename) or self.storage.is_file(dstfilename):
            connection.send_literal(tokens.ERROR_MESSAGE)
            loginfotext = "The job of client {} is not valid, the filename '{}' not exists or the dstfilename '{}' exists.".format(
                connection.get_addr(),
                filename, 
                dstfilename
                )
            connection.send_literal(loginfotext)
            logging.error(loginfotext)
            print(loginfotext)
            
        else:
            self.minions_lock.acquire()
            minionIndex = random.randrange(0, len(self.minions))
            
            minion = self.minions[minionIndex]
            
            imagedata = self.storage.get_file(filename)
            coreIndex = minion.send_job(imagedata, dstfilename, token)
            
            loginfotext = "The Job '{}' submitted successfully by ty the client {} to the core {} of the minion {}".format(
                tokens.token_to_str(token),
                connection.get_addr(),
                coreIndex,
                minion.get_addr()
                )
            
            connection.send_literal(tokens.INFO_MESSAGE)
            connection.send_literal(loginfotext)
            logging.info(loginfotext)
            print(loginfotext)
            
            self.minions_lock.release() 
        
        return True