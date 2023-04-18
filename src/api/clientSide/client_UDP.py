import socket
import json

#SERVER = '192.168.1.234' #put IPv4 address of server (beagle boa) here
#SERVER = '192.168.1.155' 
#SERVER = '192.168.1.229'
#SERVER = '192.168.8.220'
#SERVER = '10.151.129.96'
#SERVER = '10.151.143.174'
SERVER = '192.168.6.2'
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADER = 16
BYTESIZE = 1024

#connect client to server
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    # Create a dictionary representing the tuple as a JSON object
    json_obj = {'key': msg[0], 'value': msg[1]}
    
    # Serialize the dictionary to a JSON string
    json_str = json.dumps(json_obj)
    
    # Encode the JSON string to bytes
    msg = json_str.encode(FORMAT)

    client.sendto(msg, ADDR)
   
''' 
send(('left_stick', 90))
input()
send(('right_trigger', -0.5))
input()
send((DISCONNECT_MESSAGE, 'nothing'))
'''