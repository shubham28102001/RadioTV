import socket 


HOST = "127.0.0.1"
PORT = 8002 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
client_socket.connect((HOST, PORT))
print("Connected to the main server");
while True:
    data = input("Enter the message: ")
    client_socket.send(data.encode('utf-8'))
   
    print(data)



