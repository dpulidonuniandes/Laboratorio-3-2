import socket
import sys
import threading

def multiples():
    # Create a TCP/IP socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('127.0.0.1', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)    
    mensajeServidor = sock.recv(1024)
    print(mensajeServidor.decode())

    print('closing socket')

    return 

NUM_HILOS = 4

for hilo in range(NUM_HILOS):
    hilo = threading.Thread(name='hilo%s' %num_hilo, 
                            target=multiples)    
    hilo.start()
