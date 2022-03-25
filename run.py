
import eel
import socket
from tkinter.filedialog import askopenfilename

# filename = askopenfilename()

eel.init('gui')

@eel.expose
def muie():
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    return ip

eel.start('index.html', size=("1024","576"))
