import datetime
import socket
import os
from _thread import *
import tqdm
import hash
import time
IP = '192.168.1.109'
PORT = 12000
ADDR = (IP, PORT)
ThreadCount = 1
SIZE = 2048
FORMAT = "utf-8"
try:
    print("[STARTING] Server is starting.")
    """ Staring a UDP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)
except socket.error as e:
    print(str(e))    
    
""" Server is listening, i.e., server is now waiting for the client to connected. """

def multi_threaded_client(conn,cliente,direccion,filesize,num,fileLog):
    print("[LISTENING] Server is listening.")
    """ Server has accepted the connection from the client. """

    print(f"[NEW CLIENT] {cliente} connected.")

    archivo="cliente" + str(cliente) + ".txt"        
    """ Opening and reading the file data. """ 
    filename=archivo 

    file = open((direccion+filename), "r")
    

    
    """ Sending the filename to the server. """
    server.sendto(filename.encode(FORMAT),conn)
    msg, conn = server.recvfrom(SIZE)
    msg = msg.decode()


    print(f"[SERVER]: {msg}")
    """ Sending the hash to the client. """
    hashing=hash.hash_file(direccion+filename)
    server.sendto(hashing.encode(FORMAT),conn)
    """ Sending the filesize to the server. """
    print("---------------------------------------------------------//////////////////////")
    strfilesize=str(filesize)
    server.sendto(strfilesize.encode(FORMAT),conn)
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    sentinela=True
    
    fileLog.write("Archivo enviado: Cliente"+str(cliente)+"-Prueba-"+str(num)+".txt")
    fileLog.write("\n")
    fileLog.write("Tamano: "+str(filesize/1048576)+"MB")
    fileLog.write("\n")
    
    ts1=time.time()

    with open((direccion+filename), "rb") as f:
        while sentinela:
            

            # read the bytes from the file
            bytes_read = f.read(SIZE)
            if not bytes_read:
            # file transmitting is done
                sentinela=False
        # we use sendall to assure transimission in 
        # busy networks
            server.sendto(bytes_read,conn)
        # update the progress bar
            progress.update(len(bytes_read))

    fileLog.write("Entrega exitosa? "+str(not sentinela))
    fileLog.write("\n")
    ts2=time.time()
    tst=ts2-ts1
    fileLog.write("Tiempo de transferencia: "+str(tst*1000)+"ms")
    fileLog.write("\n")
    fileLog.write("\n")

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

ct = datetime.datetime.now()
ct=str(ct)
file_name="Logs/"+ct+"-log.txt"
file_name=file_name.replace(":","-")
fileLog = open(file_name, "w")
while True:
    if (ThreadCount<= num):
        Client, address = server.recvfrom(4096)
        server.sendto(Client, address)
        print(Client.decode())
        cliente=[Client, address]
        lista.append(cliente)
        print('Connected to: ' + address[0] + ':' + str(address[1]))
    if(ThreadCount == num):
        for i in range(0,num):
            multi_threaded_client(address,i+1,direccion,tamano,num,fileLog)
 
    if (ThreadCount>num):
        break



    print('Thread Number: ' + str(ThreadCount))
    ThreadCount += 1
    
fileLog.close()
server.close()

    
