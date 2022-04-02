
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
            print("Could not save settings. Settings file not found")
            exit()

        self.loadSettings()

    def returnJSON(self) -> None:
        eel.loadSettings(json.dumps(self._settingsFile))

@eel.expose()
def updateSettings(misc, colors):

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


@dataclass(init=False)
class Connections:
    """Class for keeping track of contacts and incoming connections"""

    accepted      :       dict
    pending       :       dict

    def addPending(self, clientSocket,clientAddress, clientFile):
        self.pending[clientAddress] = {
            "username"          :   clientFile["username"],
            "profilePhoto"      :   clientFile["profilePhoto"],
            "status"            :   clientFile["status"],
            "socketObj"         :   clientSocket
        }

    def moveToAccepted(self, clientAddress):
        self.accepted[clientAddress] = self.pending[clientAddress]
        self.pending.pop(clientAddress)

    def remove(self, clientAddress):
        try:
            self.accepted.pop(clientAddress)
        except:
            self.pending.pop(clientAddress)
        finally:
            print("The contract you're trying to remove does not exist")
        
class Server:
    def __init__(self):
        
        self.location = (socket.gethostbyname(socket.gethostname()), int(_SETTINGS.port))

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.socket.bind(self.location)
        except:
            print("Could not create server socket.")
            exit()

    def start(self):
        self.socket.listen(2)

        while True:
            clientSocket, clientAddr = self.socket.accept() 

            clientHandlerThread = Thread(target=self.clientHandler, args=(clientSocket, clientAddr))
            clientHandlerThread.start()

    def clientHandler(self, cSocket, cAddr):

        if cAddr not in _CONTACTS.pending.keys() and cAddr not in _CONTACTS.accepted.keys():
            cF = cSocket.recv(1024)
            _CONTACTS.addPending(cSocket, cAddr, cF)

            userFile = {
                "username":_SETTINGS.username,
                "profilePhoto":_SETTINGS.avatar,
                "status":_SETTINGS.status
            }

            userFile = json.dumps(userFile)
            cSocket.send(userFile)


        elif cAddr in _CONTACTS.accepted.keys():
            msg = cSocket.recv()
            print(msg.decode('utf-8'))
            # do something with the message


class Client:
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        except:
            print("Could not create client socket.")
            exit()
        
        self.isConnected = 0

    def connect(self, ip,port):
        try:
            self.socket.connect((ip,port))
            print(f"Connected to {ip}:{port}")
            self.isConnected = 1
        except:
            print(f"Could not connect to {ip}:{port}. User may be offline?")
    
    def sendMessage(self, message):
        self.socket.send(message.encode('utf-8'))
    
    

# Create the contact dictionary
_CONTACTS = Connections()

#Load the settings and send the JSON file to JS
_SETTINGS = Settings()
_SETTINGS.returnJSON()

#Create the internal server
_SERVER = Server() 

#Start the app
eel.start('index.html', size=("1024","640"))
