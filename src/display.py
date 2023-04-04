# Inital test usage of PySimpleGUI

import PySimpleGUI as sg
# import cv2

valueSet = 0
layout = []

#Video Capture display
# layout += [[sg.Image(key='-I-')], ]
# cap = cv2.VideoCapture(0)  # Setup the camera as a capture device

# Slider display
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
# Event Loop
while True:
    event, values= window.read(timeout=20)
    if event == sg.WIN_CLOSED:
        break
    sz_spin = int(values['spin'])
    # sz_slider = int(values['slider'])
    sz = sz_spin
    if sz != valueSet:
        valueSet = sz
        font = "Helvetica "  + str(valueSet)
        window['sliderReverse'].update(sz-100)
        window['sliderHorizontal'].update(sz*2-100)
        window['sliderForward'].update(sz)
        window['spin'].update(sz)
        
    # window['-I-'].update(data=cv2.imencode('.ppm', cap.read()[1])[1].tobytes())  # Update image in window