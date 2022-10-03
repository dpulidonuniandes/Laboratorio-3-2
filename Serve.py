import socket
import os
from _thread import *
import tqdm
import hash
IP = '127.0.0.1'
PORT = 4455
ADDR = (IP, PORT)
ThreadCount = 1
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
    """ Server has accepted the connection from the client. """

    print(f"[NEW CLIENT] {cliente} connected.")

    archivo="cliente" + str(cliente) + ".txt"        
    """ Opening and reading the file data. """ 
    filename= archivo #CAMBIAR POR UN INPUT
    print("Archivooooooo")
    print(arvhivo)
    file = open(filename, "r")
    data = file.read()
    """ Reciving the sizefile to the server. """
    tamano=conn.recv(SIZE).decode(FORMAT)
    
    """ Sending the filename to the server. """
    conn.send(filename.encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)

    print(f"[SERVER]: {msg}")
    hashing=hash.hash_file(filename)
    conn.send(hashing.encode(FORMAT))
    filesize = 104857600 #CAmbiar despues
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(SIZE)
            if not bytes_read:
                print("salio al break")
            # file transmitting is done
                break
        # we use sendall to assure transimission in 
        # busy networks
            conn.send(bytes_read)
        # update the progress bar
            progress.update(len(bytes_read))
    """ Sending the hash to the client. """
    
    print("Hash envido")
    print(hashing)
    

    """ Closing the file. """
    file.close()
        
lista=[]
while True:
    if (ThreadCount<=5):
        Client, address = server.accept()
        cliente=[Client, address]
        lista.append(cliente)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
    if(ThreadCount == 5):
        for i in range(0,5):
            multi_threaded_client(lista[i][0],i+1)
 
    if (ThreadCount>5):
        break



    print('Thread Number: ' + str(ThreadCount))
    ThreadCount += 1
server.close()
