import racer
import PySimpleGUI as sg
import client_UDP
import time
import pygame
from tkinter import Tk
root = Tk()
root.withdraw()


def getStickAngleAlt(x_axis):
    return 90 + (-90 * x_axis)


def countdown():
    for i in range(1, 0, -1):
        print(i)
        time.sleep(1)


def quitPygame():
    pygame.quit()
    exit()


'''  
Determines whether to send the current_value, depending if the difference from the last_value is over the threshold.
current_value is value output from controller
last_value was the previous value sent to the beagle board
percentThreshold is the % difference that needs to be met 
range is the range of the possible values of an input (e.g. trigger is -1 to 1 -> Range is 2)
'''


def update_last_value(current_value, last_value, percentThreshold, range):
    if last_value is None:
        return current_value

    diff = abs(current_value - last_value)
    threshold = percentThreshold * range

    if diff > threshold:
        return current_value

    return last_value

# Send the angle to the board
# Send angle = 90 if the lastAngle was relatively close to it. This is to ensure that if we let go of the left stick, the RC car gets input to stays straight.
# angleThreshold is the angle that we +/- to 90 (e.g. angleThreshold = 5 -> 90-5 and 90+5 -> 85 to 95)


def sendAngle(angleThreshold):
    if angle == None:
        return
    lowThreshold = 90 - angleThreshold
    highThreshold = 90 + angleThreshold
    if (lowThreshold < angle < highThreshold):
        res = round(90, 3)
    else:
        res = round(angle, 3)
    print(f'Sending angle: {res}')
    client_UDP.send(('angle', res))

# calcualte what throttle to send


def sendThrottle(throttleThreshold):
    if boost and not reverseBoost:
        res = 'BOOST'
    elif not boost and reverseBoost:
        res = 'REVBOOST'
    elif leftTriggerVal == None and rightTriggerVal == None:
        return
    elif leftTriggerVal == None and rightTriggerVal != None:
        res = round(rightTriggerVal + 1, 3)
    elif rightTriggerVal == None and leftTriggerVal != None:
        res = round((leftTriggerVal + 1) * -1, 3)
    else:
        triggerOutput = rightTriggerVal - leftTriggerVal
        highThreshold = 0 + throttleThreshold
        lowThreshold = 0 - throttleThreshold
        if highThreshold > triggerOutput > lowThreshold:
            res = 0
        else:
            res = round(triggerOutput, 3)
    # TODO: send throttle to RM. res * 50
    if res == 'BOOST' or res == 'REVBOOST':
        racerConnect.send_throttle(res)
    else:
        racerConnect.send_throttle(round(res * 50))
    print(f'Sending throttle value: {res}')
    client_UDP.send(('throttle', res))


def checkBoost():
    global reverseBoost
    global boost
    if joystick.get_button(9):
        reverseBoost = True
    else:
        reverseBoost = False
    if joystick.get_button(10):
        boost = True
    else:
        boost = False


# see controller object plugged in
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i)
             for i in range(pygame.joystick.get_count())]
print(joysticks)

# initalize
pygame.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# mappings for PS4 controller on mac/windows
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

# Initialize simpleGUI layout
layout = []

# Video Capture display
# layout += [[sg.Image(key='-I-')], ]
# cap = cv2.VideoCapture(0)  # Setup the camera as a capture device
layout += [[sg.Text("Speed", font="Helvetica 20", key='text'),
           sg.Slider(range=(-100, 100), orientation='v', size=(10, 20),
           enable_events=True, key='sliderReverse', font=('Helvetica 20'))],
           [sg.Text("Angle %", font="Helvetica 20", key='text'),
           sg.Slider(range=(-100, 100), orientation='h', size=(10, 20),
                     enable_events=True, key='sliderHorizontal', font=('Helvetica 20')),],
           [sg.Text("Ready signal to rm has not been sent", font="Helvetica 20", key='signal',
                    enable_events=True),]]

# Window from pySimpleGUI
windowSG = sg.Window("Controller GUI", layout, grab_anywhere=False)

countdown()

angle = None
leftTriggerVal = None
rightTriggerVal = None
boost = False
reverseBoost = False

displayLeftTrigger = 0.0
displayRightTrigger = 0.0
displayjoystickx = 0.0

readySignalSent = False  # TODO: add in Dan's code

# Racer Connection to Race Management with car creation
racerConnect = racer.RaceConnection("G17")
racerConnect.start()
# NEED TO GET UDP LINK, do racer.sendFeed to retreive.

while True:
    # To update values
    for event in pygame.event.get():
        # Buttons
        if event.type == pygame.JOYBUTTONDOWN:
            # TODO: change to "arm" esc
            if joystick.get_button(0):
                print('Sending ready signal to RM')
                client_UDP.send(('x', 0))
                readySignalSent = True
                eventSG, values = windowSG.read(timeout=20)
                windowSG['signal'].update("Ready signal to rm has been sent")
            elif joystick.get_button(3):
                print('Quitting pygame, leaving server open')
                client_UDP.send(('triangle', 0))
                quitPygame()
            elif event.button in [4, 5, 6]:
                print("Quitting pygame AND the server on the beagleboard")
                client_UDP.send((client_UDP.DISCONNECT_MESSAGE, 666))
                quitPygame()

        # Triggers/Stick
        elif event.type == pygame.JOYAXISMOTION:
            # Left trigger
            if event.axis == 4:
                leftTriggerVal = displayLeftTrigger = joystick.get_axis(4)

            # Right trigger
            elif event.axis == 5:
                rightTriggerVal = displayRightTrigger = joystick.get_axis(5)

            # Left stick -> Angle
            elif event.axis == 0 or event.axis == 1:
                angle = getStickAngleAlt(joystick.get_axis(0))
                displayjoystickx = joystick.get_axis(0)

    # Send angle [0, 180] and throttle [-2, 2]
    checkBoost()
    sendAngle(20)  # TODO: raise threshold if car isn't being kept straight
    # TODO: lower threshold is car is not responding to triggers
    sendThrottle(.1)

    # Adjust how much the pygame is updated
    clock.tick(50)

    # Update GUI
    eventSG, values = windowSG.read(timeout=20)
    if (leftTriggerVal != None & rightTriggerVal != None):
        windowSG['sliderReverse'].update(int((displayLeftTrigger+displayRightTrigger)*50))
    if (angle != None):
        windowSG['sliderHorizontal'].update(int(displayjoystickx*100))

    # windowSG['-I-'].update(data=cv2.imencode('.ppm', cap.read()[1])[1].tobytes())  # Update image in window
