import socket
import os
from _thread import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)
ThreadCount = 0
SIZE = 4096
FORMAT = "utf-8"
try:
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
    server.listen(5)
except socket.error as e:
    print(str(e))    
    
""" Server is listening, i.e., server is now waiting for the client to connected. """

def multi_threaded_client(conn,cliente):
    print("[LISTENING] Server is listening.")
    while True:
        """ Server has accepted the connection from the client. """
        
        print(f"[NEW CLIENT] {cliente} connected.")

        archivo="cliente" + str(cliente) + ".txt"        
        """ Opening and reading the file data. """ 
        filename= archivo #CAMBIAR POR UN INPUT
        file = open(filename, "r")
        data = file.read()
        """ Sending the filename to the server. """
        conn.send(filename.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        """ Sending the file data to the server. """
        conn.send(data.encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")
        """ Closing the file. """
        file.close()
        
        
while True:
    Client, address = server.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    ThreadCount += 1
    if(ThreadCount == 5):
        start_new_thread(multi_threaded_client, (Client,ThreadCount ))
    
    print('Thread Number: ' + str(ThreadCount))
server.close()
