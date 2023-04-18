import socket 
import json

SERVER = socket.gethostbyname(socket.gethostname()) # Look at "default" server
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
    print(f"[STARTING] Server is on {SERVER}")
    openServer = True
    while openServer:
        message, address = server.recvfrom(BYTESIZE)
        json_str = message.decode(FORMAT)
        
        # Deserialize the JSON string to a dictionary
        json_obj = json.loads(json_str)
        key = json_obj["key"]
        value = json_obj["value"]
        
        # print(f'[{address}] Key: {key}, Value: {value}')
        
        # If you want to send a project back to the client
        # server.sendto("Message received!".encode(FORMAT), address)
        
        '''
        TODO: Send out calls to different parts of BeagleBone.
        - If statements for different key/value pairs. 
        '''
        if key == DISCONNECT_MESSAGE: #used to close server
            openServer = False
            print(f'[ENDING] Server is closing')
        elif key == 'left_stick':
            print(f'[UPDATE] Servo, value: {value}')
        elif key == 'left_trigger':
            print(f'[UPDATE] PWM brake, value: {value}')
        elif key == 'right_trigger':
            print(f'[UPDATE] PWM accelerate, value: {value}')
        elif key == 'x':
            print(f'[ALERT] Race Management with a ready signal, value: {value}')
        elif key == 'triangle':
            print(f'[ENDING] Quitting pygame, leaving server open, value: {value}')

start()
server.close()