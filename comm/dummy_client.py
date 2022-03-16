import socket
import time as t

import random

HOST = "localhost"  # The server's hostname or IP address
PORT = 7778  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST,PORT))

HEADER = 10

while True:
    t.sleep(3)
    s.send(bytes(f"Client says hello {random.randint(0,1000)}", "utf-8"))

    print(s.recv(1024).decode("utf-8"))


    

