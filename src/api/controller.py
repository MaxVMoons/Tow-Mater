import pygame
import sys
import math

class Player(object):
    def __init__(self, color):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = color
    
    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))
    
    def change_color(self, color):
        self.color = color
    
    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)
    
    def getStickAngle(x_axis, y_axis):
        angle = math.atan2(y_axis, x_axis) * 180 / math.pi
        print ("Angle is: ", angle)

# see controller object plugged in
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

# initalize game
pygame.init()
leftStick = Player("white")
rightStick = Player("blue")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1920, 1080))
# replace with correct index in list if multiple controllersls
joystick = pygame.joystick.Joystick(0)
joystick.init()
DEADZONE = 0.1

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

# Load the PS4 controller overlay
ps4_controller_image = pygame.image.load("ps4_controller3(1000x598).png")

# run 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            False
            pygame.quit()
            exit()
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
                False
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

    #apply deadzone to sticks
    if abs(axes["left_x"]) < DEADZONE:
        axes["left_x"] = 0
    if abs(axes["left_y"]) < DEADZONE:
        axes["left_y"] = 0
    if abs(axes["right_x"]) < DEADZONE:
        axes["right_x"] = 0
    if abs(axes["right_y"]) < DEADZONE:
        axes["right_y"] = 0
    
    #get joystick values (to be sent to board)
    leftStick_x = axes["left_x"]
    leftStick_y = axes["left_y"]
    
    # move leftStick
    left_xSpeed = round(leftStick_x, 5)
    left_ySpeed = round(leftStick_y, 5)
    leftStick.move(left_xSpeed*3, left_ySpeed*3)
    
    #get joystick values for right (to be sent to board)
    rightStick_x = axes["right_x"]
    rightStick_y = axes["right_y"]

    # move player2
    right_xSpeed2 = round(rightStick_x, 5)
    right_ySpeed2 = round(rightStick_y, 5)
    rightStick.move(right_xSpeed2*3, right_ySpeed2*3)
    
    screen.fill((0, 0, 0)) # black background

    # Draw the PS4 controller image onto the display window
    screen.blit(ps4_controller_image, (-50, 500))

    leftStick.draw(screen)
    rightStick.draw(screen)
    pygame.display.update()
    clock.tick(169)

# TODO: 1) change the move function so it continuously moves in that direction (and can consistently send info to board) 
# 2) replace joystick.get_axis and joystick.get_button with the dictionary values 
# 3) clean up and note that other functions to implement to simplify code 
# 4) get the triggers to work, ensure we can gradually hold down on them
# 5) have a ps4 overlay?
# 6) calcualte angle to send over to board.