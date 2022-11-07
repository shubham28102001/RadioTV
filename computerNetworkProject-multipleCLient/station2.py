
import socket
from threading import Thread

HOST  = "10.20.36.0"
PORT = 8005
BUFFERSIZE = 1024

def station_connection():
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((HOST, PORT))
    print("socket binded to %s" %(PORT))
    while True:
       print('recieving .....')
       message,address =  client_socket.recvfrom(BUFFERSIZE)
       message = message.decode('utf-8')
       print(message)
       client_socket.sendto(str("hello from the second server").encode(),address)
new_thread = Thread(target=station_connection, args=())
new_thread.start()  





    
    