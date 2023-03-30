import socket 
# import threading

SERVER = socket.gethostbyname(socket.gethostname()) 
#SERVER = '192.168.1.234'
#SERVER = '192.168.8.153' 
#SERVER = '192.168.8.117'
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 16
BYTESIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse the same server/socket again
server.bind(ADDR)

def start():
    print(f"Server is on {SERVER}")
    openServer = True
    while openServer:
        message, address = server.recvfrom(BYTESIZE)
        print(f'[{address}] {message.decode(FORMAT)}')
        server.sendto("Message received!".encode(FORMAT), address)
        '''
        TODO: Put if statements for different messages. Send out messages to differnt parts of beagleboard.
        Also a keybind to close the server (so we don't have to crtl z)
        '''
        if (message.decode(FORMAT) == DISCONNECT_MESSAGE):
            openServer = False

print("[STARTING] server is starting...")
start()
server.close()