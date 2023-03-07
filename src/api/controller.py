import pygame
import sys
import math
import time

'''
Notes:
    * PS4 controller plugged in 
    * Countdown to check that the joystick is recognized
    * Change the clock.tick() to change speed of program
    * Angles goes from 0 to 359 counter clockwise
    * Shows angles for both sticks
    * Press PS4, share, or options button to quit. 
TODO: 
    2) replace joystick.get_axis and joystick.get_button with the dictionary values 
    4) get the triggers to work. Ensure we can gradually hold down on them
    5) have a ps4 overlay?
    6) have angle change gradually. ensure it's not jerky.
Changes:
    * Added filter to gradually change angles, but can only use one stick.
    * Added the triggers. 
'''

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
        if angle < 0: angle += 360
        print ("Angle is: ", round(angle))

def checkQuit():
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

def checkPressDown():
    # do action when button is pressed DOWN
    if event.type == pygame.JOYBUTTONDOWN:
        if joystick.get_button(0):
            print("X")
        elif joystick.get_button(1):
            print("Circle")
        elif joystick.get_button(2):
            print("Square") 
        elif joystick.get_button(3):
            print("Triangle")
        elif event.button in [4,5,6]:
            pygame.quit() 
            exit()
        elif joystick.get_button(7):
            print("Left Stick Button") 
        elif joystick.get_button(8):
            print("Right Stick Button") 
        elif joystick.get_button(9):
            print("Left Trigger")
        elif joystick.get_button(10):
            print("Right Trigger")   
        elif joystick.get_button(11):
            print("Up Button")    
        elif joystick.get_button(12):
            print("Down Button")  
        elif joystick.get_button(13):
            print("Left Button")     
        elif joystick.get_button(14):
            print("Right Button") 
        #print(event)

def moveStick(self, xAxis, yAxis, filter_val):
    global filtered_x, filtered_y
    filtered_x = filtered_x * (1 - filter_val) + xAxis * filter_val
    filtered_y = filtered_y * (1 - filter_val) + yAxis * filter_val

    xSpeed = round(xAxis, 5)
    ySpeed = round(yAxis, 5)
    self.move(xSpeed*20, ySpeed*20)
    self.getStickAngle(filtered_x, filtered_y * -1)

def countdown():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

# Gets the PS4 image object
def loadOverlay(filename):
    return pygame.image.load(filename)

# Draw the PS4 controller image onto the display window
def drawOverlay(image):
    screen.blit(image, (-50, 500))

# see controller object plugged in
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

# initalize GUI
pygame.init()
leftStick = Stick("white")
rightStick = Stick("red")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
# replace with correct index in list if multiple controllers
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

countdown()

filter_val = 0.01
filtered_x = 0
filtered_y = 0

# run 
while True:
    for event in pygame.event.get():
        checkQuit()
        checkPressDown()

        # Check for joystick axis motion
        if event.type == pygame.JOYAXISMOTION:
            # Left trigger
            if event.axis == 4:
                print("Left trigger value: ", round(joystick.get_axis(4),2))
            # Right trigger
            elif event.axis == 5:
                print("Right trigger value: ", round(joystick.get_axis(5),2))
    
    # move leftStick
    moveStick(leftStick, joystick.get_axis(0), joystick.get_axis(1), filter_val)

    # move rightStick
    #moveStick(rightStick, joystick.get_axis(2), joystick.get_axis(3), filter_val)
    
    screen.fill((0, 0, 0)) # black background
    leftStick.draw(screen)
    rightStick.draw(screen)
    pygame.display.update()
    clock.tick(50)