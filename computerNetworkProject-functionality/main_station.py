import socket
from threading import Thread



"""
We are creating mainstation from where the client talk aboutthe server on which station the client wants to connect 

"""
DECIDORARRAY = {
"PAUSE" :False,
"RESTART" : False ,
"RADIOSTATIONCHANGE" :False,
"TERMINATE" : False 
}
EARLIERVALUE  = ""

OTHER_RADIO_STATION  = {
    "PORT1" : 8004,
    "PORT2" : 8005,
    "PORT3" : 8006
}
def mainstation():
    
    HOST =  "127.0.0.1"
    PORT = 8000
    global EARLIERVALUE,DECIDORARRAY,OTHER_RADIO_STATION;

    main_station_socket  =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_station_socket.bind((HOST, PORT))
    main_station_socket.listen(100)

    
    print("Waiting for conection...")
    client_socket,address =  main_station_socket.accept()
    while True:
        print(client_socket)
        data = client_socket.recv(1024).decode()
        if data!='':
        
            print("message from the client is : ",data)
            if DECIDORARRAY.get(data)==None:
                DECIDORARRAY[EARLIERVALUE] = False
                print("NOT FOUNDED")
            else:
                DECIDORARRAY[data] = True
                if data=="RADIOSTATIONCHANGE":
                    radio_station_number = client_socket.recv(1024).decode()
                    print(radio_station_number)
                    if(OTHER_RADIO_STATION.get(radio_station_number)==None):
                        founded = 'not Founded'
                        client_socket.send(founded.encode('utf-8'))
                    else:
                        client_socket.send(str(OTHER_RADIO_STATION[radio_station_number]).encode('utf-8'))
                    print(OTHER_RADIO_STATION)
                EARLIERVALUE = data
            print("ended first loop")
            
                
new_thread = Thread(target=mainstation,args=())
new_thread.start()
# def checking():
#     global EARLIERVALUE,DECIDORARRAY
#     print(DECIDORARRAY,EARLIERVALUE)
#     while(1):
       
#         if(DECIDORARRAY.get(EARLIERVALUE)==True):
#             print(EARLIERVALUE)
# new_thread1 =Thread(target=checking,args=())
# new_thread1.start()
        


