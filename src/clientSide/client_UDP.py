import socket
import json
    
#SERVER = '192.168.1.234' #put IPv4 address of server (beagle board) here
#SERVER = '192.168.6.2' #wired, mac
SERVER = '192.168.8.153' #wireless, racer 1 board
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#connect client to server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    json_obj = {'key': msg[0], 'value': msg[1]}
    json_str = json.dumps(json_obj)
    msg = json_str.encode(FORMAT)
    client.sendto(msg, ADDR)
   
''' 
# Testing
send(('left_stick', 90))
input()
send(('right_trigger', -0.5))
input()
send((DISCONNECT_MESSAGE, 'nothing'))
'''