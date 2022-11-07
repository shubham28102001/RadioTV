# importing the library that is going to be needed
import base64
import cv2
import time
from threading import Thread
import socket
from imutils import resize
import subprocess
import pyaudio
import wave


command = "ffmpeg -i sample1.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"

subprocess.call(command, shell=True)


# declaring the filenmame
fileName = "sample1.mp4"

# getting the other component of the file
vid = cv2.VideoCapture(fileName)

# getting the frame of the video
FPS = vid.get(cv2.CAP_PROP_FPS)

print("FPS "+str(FPS))

# Time taken by the one frame
TS = 1/FPS

print("TS "+str(TS))

# Buffer size
BUFF_SIZE = 65535
WIDTH = 400

# Global variable
video = cv2.VideoCapture('sample1.mp4')
fps, st, frames_to_count, cnt = (0, 0, 20, 1)
case1, case2, case3 = False, False, False
message = b''
data = b'1'


def video_fetching():
    global WIDTH, video, fps, st, frames_to_count, cnt, message, case1, TS, case3

    """While videof file content remaining , read the data , do image resize , base64 conversion that convert data into uri 
       Calculation FPS of the video if it is low than increase it by putting less delay and vice versa
    """
    while(video.isOpened()):

        try:

            _, frame = video.read()
            frame = resize(frame, width=WIDTH)
            encoded, buffer = cv2.imencode(
                '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

            message = base64.b64encode(buffer)

            cv2.imshow("Transmitting video", frame)
            cv2.waitKey(int(TS*1000))*0xFF

            if cnt == frames_to_count:
                fps = (frames_to_count)/(time.time() - st)
                st = time.time()

                if(fps > FPS):
                    TS += 0.001
                elif (FPS > fps):
                    TS -= 0.001

                else:
                    pass

                cnt = 0
            cnt += 1

        except:

            break


t3 = Thread(target=video_fetching, args=())
t3.start()

def sendingData(server_socket,client_address,server_socket1,clientAdress,earlierdata):
    while (1):

            server_socket.sendto(message, client_address)
            if earlierdata != data and case2:
                server_socket1.sendto(data, clientAdress)
                earlierdata = data


"""
Audio and video collected data is been send to the client that are connected 
"""


def streaming():
    global message, case1, case3
    global data, BUFF_SIZE, case2
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

    server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ('192.168.0.103', 8004)
    server_socket1.bind(address)

    SOCK_ADDRESS = ("192.168.0.103", 8001)
    server_socket.bind(SOCK_ADDRESS)
    print("Listening at", SOCK_ADDRESS)
    while(1):
        nothing2, client_address = server_socket.recvfrom(BUFF_SIZE)
        nothing1, clientAdress = server_socket1.recvfrom(BUFF_SIZE)
        earlierdata = b''
        t4  = Thread(target=sendingData, args=(server_socket, client_address, server_socket1, clientAdress,earlierdata))
        t4.start()


t2 = Thread(target=streaming, args=())
t2.start()

"""
Audio fetching and giving delay to match with frame rate of the video 
"""


def audio_fetching():
    global data, case2
    waveFile = wave.open('audio.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(waveFile.getsampwidth()),
                    channels=waveFile.getnchannels(),
                    rate=waveFile.getframerate(),
                    frames_per_buffer=65535,
                    input=True)
    while len(data) > 0:
        case2 = True
        data = waveFile.readframes(10000)

        time.sleep(0.22)

    case2 = False
    stream.stop_stream()
    stream.close()
    p.terminate()


t4 = Thread(target=audio_fetching, args=())
t4.start()
