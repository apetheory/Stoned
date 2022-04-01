
import eel
import socket
import json
from dataclasses import dataclass


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


_SETTINGS = Settings()
_SETTINGS.returnJSON()

@eel.expose()
def updateSettings(misc, colors):

    _SETTINGS.username = misc[0]
    _SETTINGS.status = misc[1]
    _SETTINGS.internalServerPort = misc[2]

    _SETTINGS.colorScheme["color1"] = colors[0]
    _SETTINGS.colorScheme["color2"] = colors[1]
    _SETTINGS.colorScheme["color3"] = colors[2]
    _SETTINGS.colorScheme["color4"] = colors[3]
    _SETTINGS.colorScheme["color5"] = colors[4]
    _SETTINGS.colorScheme["color6"] = colors[5]
    _SETTINGS.colorScheme["color7"] = colors[6]
    _SETTINGS.colorScheme["color8"] = colors[7]
    _SETTINGS.colorScheme["color9"] = colors[8]
    _SETTINGS.colorScheme["color10"] = colors[9]
    _SETTINGS.colorScheme["color11"] = colors[10]


    _SETTINGS.saveSettings()
    _SETTINGS.returnJSON()




eel.start('index.html', size=("1024","640"))
