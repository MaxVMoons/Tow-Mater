import socket

HEADER = 16
SERVER = '192.168.1.234' #put IPv4 address of server (beagleboard) here
#SERVER = '192.168.8.153' 
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#connect PS4 to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TODO: test UDP on beagleboard (faster? don't need all packets)
#client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) #padding for header
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))