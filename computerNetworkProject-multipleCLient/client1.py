import base64
import socket,os
from threading import Thread
import wave, pyaudio, pickle,struct
import numpy as np
import cv2



BUFFERSIZE =  65536

HOST = "127.0.0.1"

STATION_PORT = None


def main_station_connection():
    PORT = 8000
    global STATION_PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    print("Connected to the main server")
    pause_station = []
    client_socket.connect((HOST, PORT))
   
    
    while True:
        data = input("Enter the message: ")
        client_socket.send(bytes(data, 'utf-8'))
        print("message sent")
        if(data == "RADIOSTATIONCHANGE"):
            data1 = input("Enter the station Number")
            client_socket.send(bytes(data1, 'utf-8'))
            recvData = client_socket.recv(1024).decode('utf-8')
            if(recvData == "not Founded"):
                print("Start the process again")
            STATION_PORT = int(recvData)
            print(STATION_PORT)
        elif data=="TERMINATE":
            STATION_PORT = None
            pause_station = []
        elif data=="RESTART":
            if pause_station!=[]:
                STATION_PORT = pause_station.pop()
                pause_station.append(STATION_PORT)
            else:
                print("There is no paused station")
        elif data=="PAUSE":
            pause_station.append(STATION_PORT)
            STATION_PORT = None
            
            
          


new_thread = Thread(target=main_station_connection, args=())
new_thread.start()


def other_station_port():
    global STATION_PORT
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
   
    
    while(1):
        if(STATION_PORT != None):
            client_socket.sendto("HELLO".encode('utf-8'), (HOST,STATION_PORT))
           
            while True:
                print("ewfew")
                packet,_ = client_socket.recvfrom(BUFFERSIZE)
                data = base64.b64decode(packet,' /')
                npdata = np.fromstring(data,dtype=np.uint8)
                frame = cv2.imdecode(npdata,1)
                # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                cv2.imshow("RECEIVING VIDEO",frame)
              
                try:
                        print("none")
                except:
                    
                    client_socket.close()
                    os._exit(1)
            
                   
               


new_thread1 = Thread(target=other_station_port, args=())
new_thread1.start()     
