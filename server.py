import socket 
from threading import Thread
import json


_SERVER_IP = socket.gethostbyname(socket.gethostname())
_PORT = 42706

class Server: 
    def __init__(self) -> None:
        
        # vars
        self.connectedClients = {}
            
        #Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind( (_SERVER_IP,_PORT))
        
        self.socket.listen()
        
        
    def clientHandler(self, clientSocket:object, cAddr:tuple) -> None:
        
        joinFile = clientSocket.recv(40960)
        
        joinFile = joinFile.decode("utf-8")
        joinFile = json.loads(joinFile)
        
        if(self.checkPacketValidity(joinFile)) == True:
            userFile = joinFile["content"]
            userFile["socket"] = clientSocket
             
            self.connectedClients[joinFile["uid"]] = userFile 
          
        
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
            for i in self.connectedClients:
            
                clientSocket = self.connectedClients[i]["socket"]
                
                packet = clientSocket.recv(4096)
                packet = packet.decode("utf-8")
                packet = json.loads(packet)
                print(packet)
                
                if self.checkPacketValidity(packet) == True:
                    
                    if packet["type"] == "friendRequest":
                        try:
                            
                            packet["userFile"] = self.connectedClients[i]
                      
                            packetReceiverSocket = self.connectedClients[packet["destination"]]["socket"]
                            print(packetReceiverSocket)
                            
                            packet = json.dumps(packet).encode("utf-8")
                            packetReceiverSocket.send(packet)
                            clientSocket.send(b'friend request sent :D')
                            
                        except Exception as err:
                            print(err)
                            clientSocket.send(b'could not send friend request :(')
                
                
                
        

def main() -> None:
    
    _SERVER = Server()
    threadAcceptConnections = Thread(target=_SERVER.acceptConnections)
    threadAcceptConnections.start()
    
    threadAcceptPackets = Thread(target=_SERVER.acceptPackets)
    threadAcceptPackets.start()
    
    

if __name__ == "__main__":
    main()
    
