
import socket 
from threading import Thread
import time

class internal_server:
    def __init__(self, ip, port):
        self.connections = []
        self.ip = ip
        self.port = port
        self.HEADER_SIZE = 10

        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        except:
            print("Could not create socket.")
            exit()
    
    def msg_listener(self):

        while True:
            if len(self.connections) != 0:
                for i in self.connections:
                    try:
                        packet = i.recv(1024)
                    except socket.error: 
                        print("Could not receive data, removing client")
                        self.connections.pop(self.connections.index(i))

                    if len(packet) != 0:
                        print("Packet received: "+packet.decode("utf-8"))

    def accept_conn(self):

            try:
                self.listener.bind((self.ip, self.port))
            except: 
                print(f"Could not bind server to {self.ip}:{self.port}")
                exit()
            
            self.listener.listen(1)

            # Accept new connections, add sockets to self.connections
            while True:
                clientsocket, address = self.listener.accept()
                self.connections.append(clientsocket)
                print(f"SERVER > Connection from {address}")
                clientsocket.sendall(b"Welcome!!!!")
    
    def ping_clients(self):

        while True: 
            time.sleep(5)
            print(f"Pinging {len(self.connections)} clients")

            if len(self.connections) != 0:
                for i in self.connections:
                    try:
                        i.send(b"0")
                    except socket.error:
                        print(f"Connection to {i.getsockname()} lost, disconnecting...")
                        self.connections.pop(self.connections.index(i))
    
class internal_client:
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def connect(self):
        
        ip = input("Enter ip address: ")
        port = int(input("Enter port: "))
        self.sender.connect((ip, port))

    def send_message(self, text):
        self.sender.send(text.encode("utf-8"))


Server = internal_server("0.0.0.0",7779)
Client = internal_client()

# Server related threads
SERVER_THREAD_ACCEPT_CONNS = Thread(target=Server.accept_conn)
SERVER_THREAD_MESSAGE_LISTENER = Thread(target=Server.msg_listener)
SERVER_THREAD_PING_CONNECTIONS = Thread(target=Server.ping_clients)

SERVER_THREAD_ACCEPT_CONNS.start()
SERVER_THREAD_MESSAGE_LISTENER.start()
SERVER_THREAD_PING_CONNECTIONS.start()










