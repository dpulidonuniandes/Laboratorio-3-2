import socket
import sys
import threading
import struct


def receive_file_size(sck: socket.socket):
    # Esta función se asegura de que se reciban los bytes
    # que indican el tamaño del archivo que será enviado,
    # que es codificado por el cliente vía struct.pack(),
    # función la cual genera una secuencia de bytes que
    # representan el tamaño del archivo.
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = (sck.recv(expected_bytes - received_bytes)).decode()
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize

def multiples():
    # Create a TCP/IP socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('127.0.0.1', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address) 
    print("TAMAÑO ARCHIVO")   
    print(receive_file_size(sock))
    print('closing socket')

    return 

NUM_HILOS = 4

for num_hilo in range(NUM_HILOS):
    hilo = threading.Thread(name='hilo%s' %num_hilo, 
                            target=multiples)    
    hilo.start()


