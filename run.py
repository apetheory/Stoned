
import eel
import socket
import json
from dataclasses import dataclass
from threading import Thread
import time

# filename = askopenfilename()

eel.init('gui')

_SERVER_IP      =   socket.gethostbyname(socket.gethostname()) 
_SERVER_PORT    =   42713

_UID = json.load(open("uid.json"),)["uid"]

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
def updateSettings(misc:list, colors:list) -> None:

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

    def addPending(self, UID:str, clientFile:dict) -> None:
        
        print("hello")
        
        self.pending[UID] = clientFile
        
        eel.addPending(json.dumps(self.pending[UID]))
        

    def moveToAccepted(self, UID:str) -> None:
        self.accepted[UID] = self.pending[UID]
        self.pending.pop(UID)

    def remove(self, UID:str) -> None:
        try:
            self.accepted.pop(UID)
        except:
            self.pending.pop(UID)
        finally:
            print("The contract you're trying to remove does not exist")

class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def connect(self) -> None:
        
        self.socket.connect((_SERVER_IP, _SERVER_PORT))
        
        
        clientFile = self.generatePacket(
            "newConnection",
            {"username":_SETTINGS.username,"avatar":"None","status":_SETTINGS.status}
            )

        if clientFile != None:
            
            self.socket.send(clientFile)
        
        
    def generatePacket(self, packetType:str, content:dict = {}, toWhom:str = "") -> dict:
        if packetType == "newConnection":
            packet = {
                "type":packetType,
                "uid":_UID,
                "content":content
            }
        elif packetType == "messagePacket":
            packet = {
                "type":packetType,
                "uid":_UID,
                "destination":toWhom,
                "time":time.time()*1000,
                "content":content
            }
        elif packetType == "friendRequest":
            packet = {
                "type":packetType,
                "uid":_UID,
                "destination":toWhom,
                "time":time.time()*1000
            }
        else:
            print("Invalid packet")
            return None
        
        packet = json.dumps(packet).encode("utf-8")
        
        return packet
    
    def sendData(self, packet:dict) -> None:
        
        self.socket.send(packet)
        
    def recvPacketsFromServer(self) -> None:
        
        while True: 
            packet = self.socket.recv(40960)
            packet = packet.decode("utf-8")
            packet = json.loads(packet)
            
            if self.checkPacketValidity(packet) == True:
                if packet["type"] == "friendRequest":
       
                    _CONTACTS.addPending(packet["uid"], packet["content"])
                      
    def checkPacketValidity(self, packet:dict) -> bool:
        if "type" in packet and "uid" in packet:
            return True
        else:
            return False


_CONTACTS = Connections({},{},[],{})

#Load the settings and send the JSON file to JS
_SETTINGS = Settings()
_SETTINGS.returnJSON()

_CLIENT = Client()
try:
    _CLIENT.connect()
except Exception as err:
    print("Could not connect to server. Offline?")
    print(err)

@eel.expose
def addFriend(code) -> None:
    
    if code == _UID:
        print("You cannot add yourself.")
        return
    
    _CLIENT.sendData(_CLIENT.generatePacket(
        "friendRequest",
        {},
        code
        )
    )
    

listenerThread = Thread(target=_CLIENT.recvPacketsFromServer)
listenerThread.start()

 
#Start the app
eel.start('index.html', size=("1152","640"))
