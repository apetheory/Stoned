
import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(("localhost", 6696))
s.listen(5)

HEADER = 10

clientsocket, address = s.accept()

while True: 
 
    message = input(f"Send message to {address}: ")

    message = f"{len(message):<{HEADER}}{message}"

    clientsocket.send(bytes(message, "utf-8"))
