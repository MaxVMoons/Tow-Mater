import pygame
import math
import time
import client_UDP
import PySimpleGUI as sg
# import cv2


class Stick(object):
    def __init__(self, color):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = color
    
    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))
    
    def change_color(self, color):
        self.color = color
    
    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)
    
    def getStickAngle(self, x_axis, y_axis):
        angle = math.degrees(math.atan2(y_axis, x_axis))
        if angle < 0: angle *= -1
        
        # Current range is 0-180. Put in valid angle range for servo: 
        valid_angle_min = 1.2
        valid_angle_max = 195.3

        # Map the angle to the valid angle range
        output_angle = valid_angle_min + (angle / 180.0) * (valid_angle_max - valid_angle_min)

        # Ensure the output angle stays within the valid angle range
        if output_angle > valid_angle_max:
            output_angle = valid_angle_max
        elif output_angle < valid_angle_min:
            output_angle = valid_angle_min
            
        return output_angle
           
    def moveStick(self, xAxis, yAxis):
        xSpeed = round(xAxis, 5)
        ySpeed = round(yAxis, 5)
        #self.move(xSpeed*20, ySpeed*20)
        return self.getStickAngle(xSpeed, ySpeed * -1)
    
    def getStickAngleAlt(self, x_axis, y_axis):
        return 90 + (90-1.2)*x_axis
    
    def moveStickAlt(self,xAxis, yAxis):
        
        
        return self.getStickAngleAlt(xAxis, yAxis)

def countdown():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

def quitPygame():
    pygame.quit()
    exit()

'''  
Determines whether to send the current_value, depending if the difference from the last_value is over the threshold.
current_value is value output from controller
last_value was the last_value sent to the beagle board
percentThreshold is the % difference that needs to be met 
range is the range of the possible values of an input (e.g. trigger is -1 to 1. Range is 2)
'''
def update_last_value(current_value, last_value, percentThreshold, range):
    if last_value is None:
        return current_value
    
    diff = abs(current_value - last_value)
    threshold = percentThreshold * range
    
    if diff > threshold:
        return current_value
    
    return last_value

# see controller object plugged in
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

# initalize GUI
pygame.init()
leftStick = Stick("white")
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# mappings
axes = {
    "left_x": joystick.get_axis(0),
    "left_y": joystick.get_axis(1),
    "right_x": joystick.get_axis(2),
    "right_y": joystick.get_axis(3)
}
buttons = {
    "x": 0,
    "circle": 1,
    "square": 2,
    "triangle": 3,
    "share": 4,
    "PS": 5,
    "options": 6,
    "left_stick_click": 7,
    "right_stick_click": 8,
    "L1": 9,
    "R1": 10,
    "up_arrow": 11,
    "down_arrow": 12,
    "left_arrow": 13,
    "right_arrow": 14,
    "touchpad": 15
}

#Initialize simpleGUI layout
layout = []

#Video Capture display
# layout += [[sg.Image(key='-I-')], ]
# cap = cv2.VideoCapture(0)  # Setup the camera as a capture device

layout += [[sg.Text("Reverse Trigger", font="Helvetica 20", key='text'),
           sg.Slider(range=(0, 100), orientation='v', size=(10,20),
           enable_events=True, key='sliderReverse', font=('Helvetica 20')),
           sg.Slider(range=(0, 100), orientation='v', size=(10,20),
           enable_events=True, key='sliderForward', font=('Helvetica 20')),
           sg.Text("Acceleration Trigger", font="Helvetica 20", key='text')],
          [sg.Text("Stick Horizontal Position", font="Helvetica 20", key='text'),
           sg.Slider(range=(-100, 100), orientation='h', size=(10,20),
           enable_events=True, key='sliderHorizontal', font=('Helvetica 20')),],
          [sg.Text("Ready signal to rm has not been sent", font="Helvetica 20", key='signal',
           enable_events=True),]]

#Window from pySimpleGUI
windowSG = sg.Window("Controller GUI", layout, grab_anywhere=False)

countdown()

# run 
lastAngle = None
lastLeftTrigger = None
lastRightTrigger = None

displayLeftTrigger = 0.0
displayRightTrigger = 0.0
displayjoystickx = 0.0

readySignalSent = False

while True:
    for event in pygame.event.get():
        
        # Buttons
        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(0):
                print('Sending ready signal to RM')
                client_UDP.send(('x', 0))
                readySignalSent = True
                eventSG, values= windowSG.read(timeout=20)
                windowSG['signal'].update("Ready signal to rm has been sent")
            elif joystick.get_button(3):
                print('Quitting pygame, leaving server open')
                client_UDP.send(('triangle', 0))
                quitPygame()
            elif event.button in [4,5,6]:
                print("Quitting pygame AND the server on the beagleboard")
                client_UDP.send((client_UDP.DISCONNECT_MESSAGE, 666)) 
                quitPygame()
                
        # Triggers/Stick
        elif event.type == pygame.JOYAXISMOTION:
            # Left trigger
            if event.axis == 4:
                left_trigger_value = round(joystick.get_axis(4),3)
                displayLeftTrigger = joystick.get_axis(4)
                newLeftTrigger = update_last_value(left_trigger_value, lastLeftTrigger, 0.05, 1) #Changed threshold to 0.05 input difference
                if (newLeftTrigger == lastLeftTrigger):
                  continue
                print("Sending left trigger value: ", newLeftTrigger)
                client_UDP.send(('left_trigger', newLeftTrigger))
                lastLeftTrigger = newLeftTrigger
                
            # Right trigger
            elif event.axis == 5:
                right_trigger_value = round(joystick.get_axis(5),3)
                displayRightTrigger = joystick.get_axis(5)
                newRightTrigger = update_last_value(right_trigger_value, lastRightTrigger, 0.05, 1) #Changed threshold to 0.05 input difference
                if (newRightTrigger == lastRightTrigger):
                    continue
                print("Sending right trigger value: ", newRightTrigger)
                client_UDP.send(('right_trigger', newRightTrigger))
                lastRightTrigger = newRightTrigger
                
            # Left stick -> Angle
            elif event.axis == 0 or event.axis == 1:
                left_stick_angle = int(leftStick.moveStickAlt(joystick.get_axis(0), joystick.get_axis(1)))
                displayjoystickx = joystick.get_axis(0)
                newAngle = update_last_value(left_stick_angle, lastAngle, 0.01, 180) #Changed threshold to be 10x smaller
                if (newAngle == lastAngle):
                    continue
                print(f'Sending angle: {newAngle}')
                client_UDP.send(('left_stick', newAngle))
                lastAngle = newAngle

    # Adjust how much the pygame is updated
    clock.tick(60)

    eventSG, values= windowSG.read(timeout=20)
    if(lastLeftTrigger != None):
        windowSG['sliderReverse'].update(int(displayLeftTrigger*50+50))
    if(lastAngle != None):
        windowSG['sliderHorizontal'].update(int(displayjoystickx*100))
    if(lastRightTrigger != None):
        windowSG['sliderForward'].update(int(displayRightTrigger*50+50))
    
    # windowSG['-I-'].update(data=cv2.imencode('.ppm', cap.read()[1])[1].tobytes())  # Update image in window
    
# TODO: adjust triggers to fit with motor constraints