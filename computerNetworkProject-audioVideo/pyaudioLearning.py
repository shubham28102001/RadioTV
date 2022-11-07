import pyaudio ,wave 
import socket
import os,base64,cv2
import numpy as np
from threading import Thread

def other_station_port():
    STATION_PORT = 8004
    HOST = "127.0.0.1"
    BUFFERSIZE =  65536
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


wf  = wave.open('audio.wav','rb')
p =pyaudio.PyAudio()
CHUNK = 1024
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
data =wf.readframes(CHUNK)

while len(data)>0:
    stream.write(data)
    data = wf.readframes(CHUNK)
    print(data)
    
stream.stop_stream()
stream.close()
p.terminate()
