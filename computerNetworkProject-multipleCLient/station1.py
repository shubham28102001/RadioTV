
import socket
from threading import Thread
import wave, pyaudio,pickle,struct

HOST  = "127.0.0.1"
PORT = 8004
BUFFERSIZE = 65536

def station_connection():
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((HOST, PORT))
    print("socket binded to %s" %(PORT))
    
    CHUNK = 1024
    wf = wave.open("sound.wav", 'rb')
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)
  
    while True:
        message,address =  client_socket.recvfrom(BUFFERSIZE)
    #    message = message.decode('utf-8')
    #    print(message)
    #    client_socket.sendto(str("hello from the first server").encode(),address)
        while True:
                
            data = wf.readframes(CHUNK)
            a = pickle.dumps(data)
            message = struct.pack("Q",len(a))+a
            print(message)
            client_socket.sendto(message,address)
new_thread = Thread(target=station_connection, args=())
new_thread.start()  


    
    