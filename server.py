import socket 
from threading import Thread
import json

_SERVER_IP = "192.168.50.41"
_PORT = 42713

class Server: 
    def __init__(self) -> None:
        
        # vars
        self.connectedClients = {}
        self.connectedSockets = {}

        #Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind( (_SERVER_IP,_PORT))
        
        self.socket.listen()
        
        
    def clientHandler(self, clientSocket:object, cAddr:tuple) -> None:
        
        joinFile = clientSocket.recv(16384)
        
        joinFile = joinFile.decode("utf-8")
        joinFile = json.loads(joinFile)
        
        print(joinFile)
        
        if(self.checkPacketValidity(joinFile)) == True:
            userFile = joinFile["content"]
                 
            self.connectedClients[joinFile["uid"]] = userFile 
            self.connectedSockets[joinFile["uid"]] = clientSocket
            
            Thread(target=self.acceptPackets, args=(clientSocket,joinFile["uid"])).start()
            
    def disconnectClient(self, uid:str) -> None:
        self.connectedClients.pop(uid)
        self.connectedSockets.pop(uid)
          
        
    def acceptConnections(self) -> None:
        while True:
            clientSocket, clientAddress = self.socket.accept()
            self.clientHandler(clientSocket, clientAddress)
            
    def checkPacketValidity(self, packet:dict) -> bool:
        if "type" in packet and "uid" in packet:
            return True
        else:
            return False
        
    def acceptPackets(self, clientSocket:object, uid:str) -> None:
        
        try:
            while True:  
                            
                data = clientSocket.recv(16384)
         
                if data == "": break
                
                packet = json.loads(data.decode("utf-8"))
                
                if self.checkPacketValidity(packet) != True: break
                
                print(f"Packet received: {packet}")
                
                if packet["type"] == "friendRequest":
                    
                    try:
               
                        packet["content"] = self.connectedClients[uid]
                        
                        packetReceiverSocket = self.connectedSockets[packet["destination"]]
                        print(packet)
                        packet = json.dumps(packet).encode("utf-8")
                        packetReceiverSocket.send(packet)
                        
                    except Exception as err:
                        print(f"Invalid friend code.\n{err}")
                        
        except Exception as err:
            print(f"Connection lost to client. ({err})")
            self.disconnectClient(uid)
            
                    
                                      
def main() -> None:
    
    _SERVER = Server()
    
    threadAcceptConnections = Thread(target=_SERVER.acceptConnections)
    threadAcceptConnections.start()
    
    

if __name__ == "__main__":
    main()
    
