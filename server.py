import threading
import socketserver, socket
import sys
import os
import logging, logging.handlers

TIMEOUT = 10
HOST = '192.168.117.1'
PORT = 3456

MAX_THREADS = 50

LOG_FOLDER = './Laboratorio-3'
LOG_FILE = 'socket-server.log'
ROTATE_TIME = 'midnight'
LOG_COUNT = 10

log_folder = os.path.dirname(LOG_FOLDER)

if not os.path.exists(log_folder):
 try:
  os.makedirs(log_folder)
 except Exception as error:
  print ('Error creating the log folder: %s' %error )
  exit()
try:
 logger = logging.getLogger('socket-server')
 loggerHandler = logging.handlers.TimedRotatingFileHandler(LOG_FOLDER + LOG_FILE , ROTATE_TIME, 1, backupCount=LOG_COUNT)
 formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
 loggerHandler.setFormatter(formatter)
 logger.addHandler(loggerHandler)
 logger.setLevel(logging.DEBUG)
except Exception as error:
 print ('------------------------------------------------------------------')
 print ('[ERROR] Error writing log at %s: %s' % (LOG_FOLDER, error))
 print ('[ERROR] Please verify path folder exits and write permissions')
 print ('------------------------------------------------------------------')
 exit()


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            # chequeamos el numero de threads activos. Si es mayor que el limite establecido cerramos la conexion y no atendemos al cliente. Lo trazamos
            if threading.activeCount() > MAX_THREADS:
                logger.warn('%s -- Execution threads number: %d', threading.currentThread().getName(),
                            threading.activeCount() - 1)
                logger.warn('Max threads number as been reached.')
                self.closed()
            # si no hemos alcanzado el limite lo atendemos
            else:
                threadName = threading.currentThread().getName()
                activeThreads = threading.activeCount() - 1
                clientIP = self.client_address[0]
                logger.info('[%s] -- New connection from %s -- Active threads: %d' , threadName, clientIP, activeThreads)
                data = self.request.recv(1024)
                logger.info('[%s] -- %s -- Received: %s' , threadName, clientIP, data)
                response = 'Thanks %s, message received!!' % clientIP
                self.request.send(response)
        except (Exception,error):
            if str(error) == "timed out":
                logger.error ('[%s] -- %s -- Timeout on data transmission ocurred after %d seconds.' ,threadName, clientIP, TIMEOUT)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def finish_request(self, request, client_address):
        request.settimeout(TIMEOUT)
        SocketServer.TCPServer.finish_request(self, request, client_address)
        SocketServer.TCPServer.close_request(self, request)

try:
    print ("Starting server TCP at IP %s and port %d..." % (HOST,PORT))
    server = ThreadedTCPServer((HOST, PORT), RequestHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()