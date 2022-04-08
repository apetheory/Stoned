class Server:
    def __init__(self) -> None:
        
        self.location = (socket.gethostbyname(socket.gethostname()), int(_SETTINGS.internalServerPort))

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.socket.bind(self.location)
        except:
            print("Could not create server socket.")
            exit()

    def start(self) -> None:
        self.socket.listen()

        while True:
            clientSocket, clientAddr = self.socket.accept() 

            clientHandlerThread = Thread(target=self.clientHandler, args=(clientSocket, clientAddr))
            clientHandlerThread.start()

    def clientHandler(self, cSocket, cAddr) -> None:

        if cAddr not in _CONTACTS.pending.keys() and cAddr not in _CONTACTS.accepted.keys():
            cF = cSocket.recv(1024)

            if type(cF) == dict and "username" in cF and "profilePhoto" in cF and "status" in cF and "ip" in cF and "serverPort" in cF:
                _CONTACTS.addPending(cSocket, cAddr, cF)
            else:
                print(f"Invalid clientFile received from {cAddr}: Not following format")

            userFile = {
                "username":_SETTINGS.username,
                "profilePhoto":_SETTINGS.avatar,
                "status":_SETTINGS.status,
                "serverPort":_SETTINGS.internalServerPort
            }

            userFile = json.dumps(userFile)
            cSocket.send(userFile)

        elif cAddr in _CONTACTS.accepted.keys():
            msg = cSocket.recv(1024)
            print(msg.decode('utf-8'))

class Client:
    
  
    def __init__(self,ip,port) -> None:
        
        self.isActive = False
        self.connIP = ip
        self.connPort = port
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        except:
            print("Could not create client socket.")
            exit()
            
        self.connect(self.connIP,self.connPort)
        

    def generateClientFile(self) -> dict:

        cF = { 

            "username":_SETTINGS.username,
            "profilePhoto":_SETTINGS.avatar,
            "status":_SETTINGS.status,
            "ip":socket.gethostbyname(socket.gethostname()),
            "serverPort":_SETTINGS.internalServerPort
        }

        return cF


    def connect(self, ip,port) -> None:
        try:
            self.socket.connect( (ip,int(port)) )
      
            print(f"Connected to {ip}:{port}")
            self.isConnected = True
            
            clientFile = self.generateClientFile()
            self.socket.send(json.dumps(clientFile))
            
        except Exception as err:
            print(f"Could not connect to {ip}:{port}. User may be offline?\n{err}")
