import socket
import pyaudio

# Socket
HOST = "127.0.0.1"
PORT = 5000

p = pyaudio.PyAudio()
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)

with socket.socket() as client_socket:
    
    client_socket.connect((HOST, PORT))
    

    data = client_socket.recv(50000)
    while data != "":
        try:
            data = client_socket.recv(50000)
            stream.write(data)
        except socket.error:
            print("Client Disconnected")
            break

stream.stop_stream()
stream.close()
p.terminate()

