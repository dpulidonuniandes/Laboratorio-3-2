import socket
import threading
from _thread import *
import struct
import tqdm
import os
import hash
import shutil

def multiples(numero):
    IP = '192.168.1.109'
    PORT = 12000
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 52428800
        
    """ Staring a UDP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = 'conectar'
    """ Connecting to the server. """
    
    client.sendto(message.encode(),ADDR)
    print('envio el mensaje')
    modifiedMessage, serverAddress = client.recvfrom(SIZE)
    print(" se ha hecho la conexio n con "+str(modifiedMessage))
    """ Receiving the filename from the server. """
    filename,serverAddress = client.recvfrom(SIZE)
    filename=filename.decode()
    print("[RECV] Receiving the filename.")
    file = open(filename, "w")
    client.sendto("Filename received.".encode(FORMAT),ADDR)
    

    """ Receiving the hash from the server. """
    hashing,serverAddress =client.recvfrom(SIZE)
    hashing=hashing.decode()
    print("Hash enviado \n")
    print(hashing)
    """ Receiving the filesize from the server. """
    
    size,serverAddress =client.recvfrom(SIZE)
    size=size.decode()
    size = size[0:9]
    filesize=0
    if("104857600"==size):
        filesize=104857600
    elif("262144000"==size):
        filesize=262144000
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    
    file_stats= os.stat(filename)
    with open(filename, "wb") as f:
        while (file_stats.st_size!=filesize) :
            # read 1024 bytes from the socket (receive)
            bytes_read ,serverAddress =client.recvfrom(SIZE)
            
            if not bytes_read:    
                
                
                
                
                
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    """ Receiving the hash from the server. """   
    
 
    hashcalculado=hash.hash_file(filename)
    print("Hash calculado \n")
    print(hashcalculado)
    print("Hash")
    if (hashing==hashcalculado):
        print("El hash enviado y el hash calculado son los mismos")
    else:
         print("Los hash son distintos")
        
    
    
    print(" Receiving the file data.")

    """Closing the file. """
    
    """Closing the connection from the client. """
    client.close()
    print(f"[DISCONNECTED]disconnected.")
    nuevo="-prueba-"+str(numero)+".txt"
    cambio=filename.replace(".txt",nuevo)
    file.close()
    os.rename(filename, cambio)
    os.replace(cambio,"ArchivosRecibidos/"+cambio)
    

    
    return
    

clientes=int(input("Escriba el numero de clientes que desea conectar: \n 1)1  \n 2)5 \n 3)10 \n"))
if(clientes==1):
    clientes=1
elif(clientes==2):
    clientes=5
elif (clientes==3):
    clientes=10
    
    
NUM_HILOS = clientes

for num_hilo in range(NUM_HILOS):
    try:
        start_new_thread(multiples,(NUM_HILOS,))  
    except socket.error as e:
        print(str(e))
     
   
