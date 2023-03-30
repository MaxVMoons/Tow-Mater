import socket

#SERVER = '192.168.1.234' #put IPv4 address of server (beagleboard) here
SERVER = '192.168.8.153' 
#SERVER = '192.168.1.229'
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 16
BYTESIZE = 1024

#connect client to server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    msg = msg.encode(FORMAT)
    client.sendto(msg, ADDR)
    #confirmMSG = client.recvfrom(BYTESIZE)
    #print(f'[{confirmMSG[1]}]: {confirmMSG[0].decode(FORMAT)}')