import socket
import threading
from _thread import *



def multiples():
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4455
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 4096
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """ Connecting to the server. """
    client.connect(ADDR)
    """ Receiving the filename from the client. """
    filename = client.recv(SIZE).decode(FORMAT)
    print(filename)
    print("[RECV] Receiving the filename.")
    file = open(filename, "w")
    client.send("Filename received.".encode(FORMAT))
    """ Receiving the file data from the client. """
    data = client.recv(SIZE).decode(FORMAT)
    print(" Receiving the file data.")
    file.write(data)
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
     
   
