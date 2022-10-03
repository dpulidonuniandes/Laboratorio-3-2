import socket
import threading
from _thread import *
import struct
import tqdm
import os
import hash

def multiples():
    IP = '127.0.0.1'
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 4096
    
    """
    tamano = int(input("defina con cuantos megabytes quiere trabajar (100 o 250): "))
    tamano = tamano*1000000
    
    
    tamano=104857600
    
    peso="" + str(tamano) + ""
    """
    
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """ Connecting to the server. """
    client.connect(ADDR)
    
    
    """ Receiving the filename from the server. """
    filename = client.recv(SIZE).decode(FORMAT)
    print(filename)
    print("[RECV] Receiving the filename.")
    file = open(filename, "w")
    client.send("Filename received.".encode(FORMAT))
    

    """ Receiving the hash from the server. """
    hashing=client.recv(SIZE).decode(FORMAT)
    print("Hash enviado \n")
    print(hashing)
    """ Receiving the filesize from the server. """
    
    filesize = int(client.recv(SIZE).decode(FORMAT)  )
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while os.path.getsize(filename)!=filesize:
            # read 1024 bytes from the socket (receive)
            bytes_read = client.recv(SIZE)
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
    if (hashing==hashcalculado):
        print("El hash enviado y el hash calculado son los mismos")
    else:
         print("Los hash son distintos")
        
    
    
    print(" Receiving the file data.")
    #file.write(data)
    client.send("File data received".encode(FORMAT))
    
    """ Closing the file. """
    """file.close()"""
    """ Closing the connection from the client. """
    """client.close()
    print(f"[DISCONNECTED]disconnected.") """
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
        start_new_thread(multiples,())  
    except socket.error as e:
        print(str(e))
     
   
