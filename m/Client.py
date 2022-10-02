import socket
import threading
from _thread import *
import struct
import tqdm
import os


def multiples():
    IP = '192.168.1.109'
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 4096
    
    """
    tamano = int(input("defina con cuantos megabytes quiere trabajar (100 o 250): "))
    tamano = tamano*1000000
    """
    
    tamano=104857600
    peso="" + str(tamano) + ""
    
    
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    """ Connecting to the server. """
    client.connect(ADDR)
    client.send(peso.encode(FORMAT))
    
    """ Receiving the filename from the server. """
    filename = client.recv(SIZE).decode(FORMAT)
    print(filename)
    print("[RECV] Receiving the filename.")
    file = open(filename, "w")
    client.send("Filename received.".encode(FORMAT))
    
    """ Receiving the file data from the server. """
    filesize = tamano  
        
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while os.path.getsize(filename)<=filesize:
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
        
        
    """ 
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    
    while received_bytes < tamano:
        data = client.recv(expected_bytes - received_bytes)
        data = data.decode(FORMAT)
        stream += data
        received_bytes += len(data)
        
        
        
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize
    """
    
    
    print(" Receiving the file data.")
    #file.write(data)
    client.send("File data received".encode(FORMAT))
    
    """ Closing the file. """
    """file.close()"""
    """ Closing the connection from the client. """
    """client.close()
    print(f"[DISCONNECTED]disconnected.") """
    return

NUM_HILOS = 5

for num_hilo in range(NUM_HILOS):
    try:
        
        start_new_thread(multiples,())  
    except socket.error as e:
        print(str(e))
     
   
