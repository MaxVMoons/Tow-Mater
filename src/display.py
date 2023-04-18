# Testing async window, see if can have a slider
# that can adjust

import PySimpleGUI as sg
import pygame
# import cv2

valueSet = 0
layout = []

#Video Capture display
# layout += [[sg.Image(key='-I-')], ]
# cap = cv2.VideoCapture(0)  # Setup the camera as a capture device

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
pygame.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()

layout += [[sg.Spin([sz for sz in range(0, 101)], font=('Helvetica 20'), initial_value=valueSet, enable_events=True, key='spin'),],
          [sg.Text("Reverse Trigger", font="Helvetica 20", key='text'),
           sg.Slider(range=(-100, 0), orientation='v', size=(10,20),
           enable_events=True, key='sliderReverse', font=('Helvetica 20')),
           sg.Slider(range=(0, 100), orientation='v', size=(10,20),
           enable_events=True, key='sliderForward', font=('Helvetica 20')),
           sg.Text("Acceleration Trigger", font="Helvetica 20", key='text')],
          [sg.Text("Stick Horizontal Position", font="Helvetica 20", key='text'),
           sg.Slider(range=(-100, 100), orientation='h', size=(10,20),
           enable_events=True, key='sliderHorizontal', font=('Helvetica 20')),]]

sz = valueSet
window = sg.Window("Slider GUI Test", layout, grab_anywhere=False)
lastAngle = 0
lastLeftTrigger = 0
lastRightTrigger = 0
# Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Left trigger
            if event.axis == 4:
                left_trigger_value = round(joystick.get_axis(4),2)
                if lastLeftTrigger == None: 
                    lastLeftTrigger = left_trigger_value
                
                else:
                    lastLeftTrigger = left_trigger_value
                    print(f'Left Trigger: {lastLeftTrigger}')
            # Right trigger
            elif event.axis == 5:
                right_trigger_value = round(joystick.get_axis(5),2)
                if lastRightTrigger == None:
                    lastRightTrigger = right_trigger_value
                elif (abs(right_trigger_value - lastRightTrigger) < .05 * 2):
                    continue
                else: 
                    lastRightTrigger = right_trigger_value
                    print(f'Right trigger: {lastRightTrigger}')
            # Left stick
            elif event.axis == 0 or event.axis == 1:
                left_stick_value = joystick.get_axis(0)
                if lastAngle == None:
                    lastAngle = left_stick_value
                elif (abs(left_stick_value - lastAngle) < .05 * 2):
                    continue
                else:
                    lastAngle = left_stick_value
                    print(f'Left stick x: {lastAngle}')
    
    for event in sg.event.get():
        values= window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            break
        sz_spin = int(values['spin'])
        # sz_slider = int(values['slider'])
        sz = sz_spin
        valueSet = sz
        font = "Helvetica "  + str(valueSet)
        window['sliderReverse'].update(-1*int(lastLeftTrigger*50+50))
        window['sliderHorizontal'].update(int(lastAngle*100))
        window['sliderForward'].update(int(lastRightTrigger*50+50))
        window['spin'].update(sz)
        
    # window['-I-'].update(data=cv2.imencode('.ppm', cap.read()[1])[1].tobytes())  # Update image in window
