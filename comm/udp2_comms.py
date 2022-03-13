import socket
import threading

ip_addr = "localhost"
l_port = 6319
s_port = 6318


def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', l_port))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', s_port))

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip_addr, s_port))