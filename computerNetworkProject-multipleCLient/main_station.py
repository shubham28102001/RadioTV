
import socket
from threading import Thread
import ast


"""
We are creating mainstation from where the client talk aboutthe server on which station the client wants to connect 

"""

# Function that are going to be used
DECIDORARRAY = {
    "PAUSE": False,
    "RESTART": False,
    "RADIOSTATIONCHANGE": False,
    "TERMINATE": False
}


EARLIERVALUE = ""

# Static station value 
OTHER_RADIO_STATION = {
    "ADDRESS1": "127.0.0.1:8001:8004",
    "ADDRESS2": "127.0.0.1:8002:8005",
    "ADDRESS3": "127.0.0.1:8006:8003"

}

# This station is used for onnecting with the necesary port 
def mainstation():
    
    
    # IP and PORT 
    HOST = "127.0.0.1"
    PORT = 8000
   
    #Socket connection
    main_station_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_station_socket.bind((HOST, PORT))
    main_station_socket.listen(100)
    
    
    print("Waiting for conection...")
    
    # If socket is conected than the 
    while True:
        client_socket, address = main_station_socket.accept()
        Thread(target=messaging, args=(client_socket,)).start()


# This function is going to run after the socket connection is done 
def messaging(client_socket):
    global EARLIERVALUE, DECIDORARRAY, OTHER_RADIO_STATION
    while True:

        data = client_socket.recv(1024).decode()
        
        # If client request for the RadiostationChange than send the port to the client if station exist 
        if data != '':

            print("message from the client is : ", data)
            
            
            if DECIDORARRAY.get(data) == None:
                DECIDORARRAY[EARLIERVALUE] = False
                print("NOT FOUNDED")
            else:
                DECIDORARRAY[data] = True
                if data == "RADIOSTATIONCHANGE":
                    radio_station_number = client_socket.recv(1024).decode()
                    if(OTHER_RADIO_STATION.get(radio_station_number) == None):
                        founded = 'not Founded'
                        client_socket.send(founded.encode('utf-8'))
                    else:
                        client_socket.send(
                            str(OTHER_RADIO_STATION[radio_station_number]).encode('utf-8'))
                EARLIERVALUE = data
                



new_thread = Thread(target=mainstation, args=())
new_thread.start()
