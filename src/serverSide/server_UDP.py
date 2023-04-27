import socket 
import json
import steering
import motor

#SERVER = socket.gethostbyname(socket.gethostname()) # Look at "default" server
#SERVER = '192.168.8.153' # racer 1, through modem
SERVER = '192.168.6.2' # mac laptop
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
BYTESIZE = 1024
startSignal = 0 # TODO: update to 1 when RM approves. Then, we can control the car

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse the same server/socket again
server.bind(ADDR)
    
def start():
    
    # Create objects for the beagleboard. TODO: move inside while loop, don't iniitalize until startSignal = 1
    steeringMotor = steering.Steering()
    throttleMotor = motor.Motor()
    
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
        
        # If you want to send a message back to the client
        # server.sendto("Message received!".encode(FORMAT), address)
        
        if key == DISCONNECT_MESSAGE: #used to close server
            openServer = False
            print(f'[ENDING] Server is closing')
            #TODO: set steeringMotor and throttleMotor to off positions and close them.
        elif key == 'angle':
            #print(f'[UPDATE] Servo, value: {value}')
            steeringMotor.changeAngle(value)
        elif key == 'throttle':
            #print(f'[UPDATE] PWM, value: {value}')
            throttleMotor.changeThrottle(value)
        elif key == 'x':
            print(f'[ALERT] Race Management with a ready signal, value: {value}')
            startSignal = 1
        elif key == 'triangle':
            print(f'[ENDING] Quitting pygame, leaving server open, value: {value}')

start()
server.close()