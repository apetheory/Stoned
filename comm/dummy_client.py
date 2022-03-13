import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 6696  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST,PORT))

HEADER = 10

receive_packet = True
packet_content = ""
packets = []

while True:
    packet = s.recv(32)
    if receive_packet == True: 
        packet_length = int(packet.decode("utf-8")[:10].strip())
        receive_packet = False
    
    packet_content += packet.decode("utf-8")

    if len(packet_content)-HEADER == packet_length:

        print(packet_content[HEADER:])
        receive_packet = True
        packet_content = ""

