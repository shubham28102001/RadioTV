import base64
import struct
import os
# from copyreg import pickle
import cv2
import time
from threading import Thread
import socket
import pyaudio
from imutils import resize
import numpy as np

# Buffer size
BUFF_SIZE = 65535

# Variable declaration in global context
IP = ""
AUDIO_PORT = None
VIDEO_PORT = None
CASE1 = 1
CASE2 = 0


def video_stream(IP, VIDEO_PORT):
    global CASE1, CASE2

    """
    Creating socket that recieve the data from the station 
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    # Sending some raw message to the radio station for indicating that client is connected to tyour station
    client_socket.sendto(b'HELLO', (IP, VIDEO_PORT))

    #  If the user has not paused the video thatn the client should decode the dataURI and covert it into numpy array
    # And then show it into the screen of the user
    while(1):

        if CASE1:
            print("CASE1")
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet)
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)

            cv2.imshow("Recieveing video", frame)
            cv2.waitKey(1)
        if CASE2:
            client_socket.close()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break

        else:
            frame = cv2.imdecode(npdata, 1)

            cv2.imshow("Recieveing video", frame)
            cv2.waitKey(1)

# For getting audio from the radioStation


def audio_stream(IP, AUDIO_PORT):
    global CASE1, CASE2

    # creating socket and Sending some raw message to the radio station for indicating that client is connected to tyour station
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b'HELLO', (IP, AUDIO_PORT))

    #  setting the pyaudio variable that convert the binary string that come from the server to the audio format
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=BUFF_SIZE)

    #  From this you are going to the recieve the binary message and than we produce sound form it
    while (1):
        if CASE1:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            stream.write(packet)
        if CASE2:
            client_socket.close()

            break


# Function used for the splitting the data that is coming from the main_station so that client can connect to any radio station
def split_recv_data(recvData):
    global IP, CASE1, AUDIO_PORT, VIDEO_PORT

    STRING_SPLITATION = recvData.split(":")

    IP = str(STRING_SPLITATION[0])
    VIDEO_PORT = int(str(STRING_SPLITATION[1]))
    AUDIO_PORT = int(str(STRING_SPLITATION[2]))

    t1 = Thread(target=video_stream, args=(IP, VIDEO_PORT))
    t2 = Thread(target=audio_stream, args=(IP, AUDIO_PORT))

    t2.start()
    t1.start()

# Connecting to the main station for getting the data of radiostation and handling other stuff like restart , Pause, Terminate


def connecting_to_main_station():
    pause_station = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.103', 8000))
    global IP, CASE1, AUDIO_PORT, VIDEO_PORT, CASE2
    while (1):
        data = input("Enter the message: ")
        client_socket.send(bytes(data, 'utf-8'))

        if(data == "RADIOSTATIONCHANGE"):
            CASE2 = 0
            data1 = input("Enter the station Number : ")
            client_socket.send(bytes(data1, 'utf-8'))
            recvData = client_socket.recv(1024).decode('utf-8')
            if(recvData == "not Founded"):
                print("Start the process again")
            split_recv_data(recvData)
        elif data == "TERMINATE":
            CASE2 = 1
            STATION_PORT = None
            pause_station = []
         
        elif data == "RESTART":
            CASE2 = 0
            if pause_station != []:
                STATION_PORT = pause_station.pop()
                pause_station.append(STATION_PORT)
                print(pause_station)
                CASE1 = 1
                split_recv_data(STATION_PORT)

            else:
                print("There is no paused station")
        elif data == "PAUSE":
            if IP != "":
                pause_station.append(
                    IP+":"+str(VIDEO_PORT)+":"+str(AUDIO_PORT))
                CASE1 = 0


t3 = Thread(target=connecting_to_main_station, args=())
t3.start()
