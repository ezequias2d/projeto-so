import server
import os
import logging

path = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(path+'connection.log')
FORMAT = '%(asctime)s\n%(levelname)s - %(message)s\n'
logging.basicConfig(filename=path+'/connection.log', encoding='utf-8', level=logging.DEBUG, format=FORMAT)

server = server.Server()

server.start()