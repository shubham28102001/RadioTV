import socket
import pyaudio

# Socket
HOST = "127.0.0.1"
PORT = 5000

# Audio
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording")

with socket.socket() as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print("Connection from " + address[0] + ":" + str(address[1]))
    while True:
        data = stream.read(CHUNK)
        conn.send(data)
        print(data)

# Audio
