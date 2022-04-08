import socket 
from threading import Thread
import json


_SERVER_IP = socket.gethostbyname(socket.gethostname())
_PORT = 42697

class Server: 
    def __init__(self) -> None:
        
        # vars
        self.connectedClients = {}
            
        #Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind( (_SERVER_IP,_PORT))
        
        self.socket.listen()
        
        
    def clientHandler(self, clientSocket : object, cAddr : tuple) -> None:
        
        joinFile = clientSocket.recv(1024)
        joinFile = joinFile.decode("utf-8")
        joinFile = json.loads(joinFile)
        print(joinFile)
        
    
    def acceptConnections(self) -> None:
        while True:
            clientSocket, clientAddress = self.socket.accept()
            self.clientHandler(clientSocket, clientAddress)
            
    def checkPacketValidity(self, packet:dict) -> bool:
        pass 
            
    def acceptPackets(self) -> None:
        pass
        
        
    

def main() -> None:
    
    _SERVER = Server()
    threadAcceptConnections = Thread(target=_SERVER.acceptConnections)
    threadAcceptConnections.start()
    
    threadAcceptPackets = Thread(target=_SERVER.acceptPackets)
    threadAcceptPackets.start()
    
    

if __name__ == "__main__":
    main()
    
