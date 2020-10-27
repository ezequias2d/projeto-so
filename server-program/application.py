import server
import os
import logging
import datetime


filename_log = 'resources/{}.log'.format(datetime.datetime.now()).replace(' ', '').replace(':', '_')

FORMAT = '%(asctime)s\n%(levelname)s - %(message)s\n'
logging.basicConfig(handlers=[logging.FileHandler(filename_log, 'w', 'utf-8')],
    format=FORMAT,
    level=logging.DEBUG)

host = input("Host: ")
server = server.Server(host)

server.start()