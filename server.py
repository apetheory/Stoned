import socket 
from threading import Thread
import json

_SERVER_IP = socket.gethostbyname(socket.gethostname())
_PORT = 42707

class Server: 
    def __init__(self) -> None:
        
        # vars
        self.connectedClients = {}
        self.connectedSockets = []

            
        #Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind( (_SERVER_IP,_PORT))
        
        self.socket.listen()
        
        
    def clientHandler(self, clientSocket:object, cAddr:tuple) -> None:
        
        joinFile = clientSocket.recv(40960)
        
        joinFile = joinFile.decode("utf-8")
        joinFile = json.loads(joinFile)
        
        print(joinFile)
        
        if(self.checkPacketValidity(joinFile)) == True:
            userFile = joinFile["content"]
            userFile["socket"] = clientSocket
             
            self.connectedClients[joinFile["uid"]] = userFile 
            self.connectedSockets.append([joinFile["uid"],clientSocket])
          
        
    def acceptConnections(self) -> None:
        while True:
            clientSocket, clientAddress = self.socket.accept()
            self.clientHandler(clientSocket, clientAddress)
            
    def checkPacketValidity(self, packet:dict) -> bool:
        if "type" in packet and "uid" in packet:
            return True
        else:
            return False
        
            
    def acceptPackets(self) -> None:
        while True:  
            for i in self.connectedSockets:
            
                clientSocket = i[1]
                
                packet = clientSocket.recv(4096)
                packet = packet.decode("utf-8")
                packet = json.loads(packet)
                
                
                if self.checkPacketValidity(packet) == True:
                    
                    print(f"Packet received: {packet}")
                    
                    if packet["type"] == "friendRequest":
                        
                        receiver = self.connectedClients[packet["destination"]]
                        

                        packetReceiverSocket = receiver["socket"]
                        
                        packet = json.dumps(packet).encode("utf-8")
                        packetReceiverSocket.send(packet)
                        clientSocket.send(b'friend request sent :D')
                        
                                      

def main() -> None:
    
    _SERVER = Server()
    
    threadAcceptConnections = Thread(target=_SERVER.acceptConnections)
    threadAcceptConnections.start()
    
    threadAcceptPackets = Thread(target=_SERVER.acceptPackets)
    threadAcceptPackets.start()
    
    

if __name__ == "__main__":
    main()
    
