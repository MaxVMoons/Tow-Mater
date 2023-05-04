import socket 
import json
import steering
import motor
#import camera

#SERVER = socket.gethostbyname(socket.gethostname()) # Look at "default" server
#SERVER = '192.168.8.153' # racer 1, through modem
SERVER = '192.168.6.2' # mac laptop
PORT = 6969
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
BYTESIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse the same server/socket again
server.bind(ADDR)
    
def start():
    steeringMotor = None
    throttleMotor = None
    
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
            if steeringMotor != None:
                steeringMotor.changeAngle(90.0)
                steeringMotor.stopMotor()
            if throttleMotor != None:
                #throttleMotor.changeThrottle(0.0) #TODO: fix later
                throttleMotor.stopMotor()
        elif key == 'angle' and steeringMotor != None:
            #print(f'[UPDATE] Servo, value: {value}')
            steeringMotor.changeAngle(value)
        elif key == 'throttle' and throttleMotor != None:
            #print(f'[UPDATE] PWM, value: {value}')
            throttleMotor.changeThrottle(value)
        elif key == 'setup' and steeringMotor == None and throttleMotor == None:
            print(f'Starting up steering and throttle objects')
            steeringMotor = steering.Steering()
            throttleMotor = motor.Motor()
        elif key == 'quitpygame':
            print(f'[ENDING] Quitting pygame, leaving server open, value: {value}')

start()
server.close()