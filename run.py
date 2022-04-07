
import eel
import socket
import json
from dataclasses import dataclass
from threading import Thread

# filename = askopenfilename()

eel.init('gui')


@dataclass
class Settings:
    """Class for keeping track of the user settings"""
    username                :       str
    status                  :       str
    avatar                  :       str
    colorScheme             :       list
    internalServerPort      :       int
    _settingsFile           :       dict

    def __init__(self) -> None:
        self.loadSettings()

    def loadSettings(self) -> None:
        try:
            with open("settings.json",) as s:
                self._settingsFile     =   json.load(s)

            self.username              =   self._settingsFile.get("username")
            self.status                =   self._settingsFile.get("status")
            self.avatar                =   self._settingsFile.get("avatar")
            self.colorScheme           =   self._settingsFile.get("colorScheme")
            self.internalServerPort    =   self._settingsFile.get("internalServerPort")

        except:
            print("Settings file not found.")
            exit()

    def saveSettings(self) -> None:

        self._settingsFile = {
            "username"              :       self.username,
            "status"                :       self.status,
            "avatar"                :       self.avatar,
            "internalServerPort"    :       self.internalServerPort,
            "colorScheme"           :       self.colorScheme
        }

        try:
            with open("settings.json","w") as s:
                s.write(json.dumps(self._settingsFile))
        except: 
            print("Could not save settings.")
            exit()

        self.loadSettings()

    def returnJSON(self) -> None:
        eel.loadSettings(json.dumps(self._settingsFile))

@eel.expose()
def updateSettings(misc, colors) -> None:

    _SETTINGS.username = misc[0]
    _SETTINGS.status = misc[1]
    _SETTINGS.internalServerPort = misc[2]

    _SETTINGS.colorScheme["color1"]     =    colors[0]
    _SETTINGS.colorScheme["color2"]     =    colors[1]
    _SETTINGS.colorScheme["color3"]     =    colors[2]
    _SETTINGS.colorScheme["color4"]     =    colors[3]
    _SETTINGS.colorScheme["color5"]     =    colors[4]
    _SETTINGS.colorScheme["color6"]     =    colors[5]
    _SETTINGS.colorScheme["color7"]     =    colors[6]
    _SETTINGS.colorScheme["color8"]     =    colors[7]
    _SETTINGS.colorScheme["color9"]     =    colors[8]
    _SETTINGS.colorScheme["color10"]    =    colors[9]
    _SETTINGS.colorScheme["color11"]    =    colors[10]


    _SETTINGS.saveSettings()
    _SETTINGS.returnJSON()


@dataclass
class Connections:
    """Class for keeping track of contacts and incoming connections"""

    accepted      :       dict 
    pending       :       dict 
    clients       :       list
    active        :       dict 

    def addPending(self, clientAddress, clientFile) -> None:
        self.pending[clientAddress] = {
            "username"          :   clientFile["username"],
            "profilePhoto"      :   clientFile["profilePhoto"],
            "status"            :   clientFile["status"],
            "serverPort"        :   clientFile["serverPort"]
        }

    def moveToAccepted(self, clientAddress) -> None:
        self.accepted[clientAddress] = self.pending[clientAddress]
        self.pending.pop(clientAddress)

    def remove(self, clientAddress) -> None:
        try:
            self.accepted.pop(clientAddress)
        except:
            self.pending.pop(clientAddress)
        finally:
            print("The contract you're trying to remove does not exist")
        
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
            # do something with the message


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
            self.socket.connect((ip,port))
            print(f"Connected to {ip}:{port}")
            self.isConnected = True
            
            clientFile = self.generateClientFile()
            self.socket.send(json.dumps(clientFile))
        except:
            print(f"Could not connect to {ip}:{port}. User may be offline?")

            
# Create the contact dictionary
_CONTACTS = Connections({},{},[],{})

#Load the settings and send the JSON file to JS
_SETTINGS = Settings()
_SETTINGS.returnJSON()

#Create the internal server
_SERVER = Server() 

def startServer() -> None:
    _SERVER.start()

startServerThread = Thread(target=startServer)
startServerThread.start()

def createClientObj(ip,port) -> None:
    try:
        clientObj = Client(ip,port)
        _CONTACTS.clients.append(clientObj)
    except Exception as err:
        print(f"Could not generate client object\n{err}")
        
@eel.expose
def connectToPeer(location) -> None:
    ip = location.split(":")[0]
    port = location.split(":")[1]
    print(f"Connecting to {ip}:{port} ..")
    
    clientThread = Thread(target=createClientObj, args=(ip,port))
    clientThread.start()

#Start the app
eel.start('index.html', size=("1152","640"))
