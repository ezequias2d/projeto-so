import server
import socket

host = input("Host: ")
server = server.Server(host)

server.start()