import socket
import os
from _thread import *
import tqdm
import hash
IP = '192.168.1.106'
PORT = 4455
ADDR = (IP, PORT)
ThreadCount = 1
SIZE = 5242880*10
FORMAT = "utf-8"
try:
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
    server.listen(25)
except socket.error as e:
    print(str(e))    
    
""" Server is listening, i.e., server is now waiting for the client to connected. """

def multi_threaded_client(conn,cliente,direccion,filesize):
    print("[LISTENING] Server is listening.")
    """ Server has accepted the connection from the client. """

    print(f"[NEW CLIENT] {cliente} connected.")

    archivo="cliente" + str(cliente) + ".txt"        
    """ Opening and reading the file data. """ 
    filename=archivo #CAMBIAR POR UN INPUT

    file = open((direccion+filename), "r")
    data = file.read()

    
    """ Sending the filename to the server. """
    conn.send(filename.encode(FORMAT))
    msg = conn.recv(SIZE).decode(FORMAT)



    print(f"[SERVER]: {msg}")
    """ Sending the hash to the client. """
    hashing=hash.hash_file(direccion+filename)
    conn.send(hashing.encode(FORMAT))
    """ Sending the filesize to the server. """
    print("---------------------------------------------------------//////////////////////")
    strfilesize=str(filesize)
    conn.send(strfilesize.encode(FORMAT))
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    sentinela=True
    with open((direccion+filename), "rb") as f:
        while sentinela:
            # read the bytes from the file
            bytes_read = f.read(SIZE)
            if not bytes_read:
            # file transmitting is done
                sentinela=False
        # we use sendall to assure transimission in 
        # busy networks
            conn.send(bytes_read)
        # update the progress bar
            progress.update(len(bytes_read))
    

    

    """ Closing the file. """
    file.close()
    
    
num=int(input("Escriba el numero de clientes que desea conectar: \n 1)1  \n 2)5 \n 3)10 \n"))
if(num==1):
    num=1
elif(num==2):
    num=5
elif (num==3):
    num=10 
direccion=int(input("Escriba el tamaño del archivo que mandara: \n 1)100MB  \n 2)250MB \n"))
tamano=0
if(direccion==1):
    direccion="archivos/100/"
    tamano=104857600 
elif(direccion==2):
    direccion="archivos/250/"
    tamano=262144000
lista=[]
while True:
    if (ThreadCount<= num):
        Client, address = server.accept()
        cliente=[Client, address]
        lista.append(cliente)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
    if(ThreadCount == num):
        for i in range(0,num):
            multi_threaded_client(lista[i][0],i+1,direccion,tamano)
 
    if (ThreadCount>num):
        break



    print('Thread Number: ' + str(ThreadCount))
    ThreadCount += 1
server.close()
