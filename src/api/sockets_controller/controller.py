import pygame
import math
import time
import client_UDP

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
        return angle
    
    def moveStick(self, xAxis, yAxis):
        xSpeed = round(xAxis, 5)
        ySpeed = round(yAxis, 5)
        #self.move(xSpeed*20, ySpeed*20)
        return self.getStickAngle(xSpeed, ySpeed * -1)

def countdown():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

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

countdown()

# run 
lastAngle = None
lastLeftTrigger = None
lastRightTrigger = None
while True:
    for event in pygame.event.get():
        # Buttons
        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(0):
                print("Sending X")
                client_UDP.send("X")
            elif joystick.get_button(3):
                print("Quitting pygame, leaving server open")
                client_UDP.send("Triangle")
                pygame.quit()
                exit()
            elif event.button in [4,5,6]:
                print("Quitting")
                client_UDP.send(client_UDP.DISCONNECT_MESSAGE) 
                pygame.quit()
                exit()
        # Triggers/Stick
        elif event.type == pygame.JOYAXISMOTION:
            # Left trigger
            if event.axis == 4:
                left_trigger_value = round(joystick.get_axis(4),2)
                if lastLeftTrigger == None: 
                    lastLeftTrigger = left_trigger_value
                elif (abs(left_trigger_value - lastLeftTrigger) < .05 * 2):
                    continue
                else:
                    lastLeftTrigger = left_trigger_value
                print("Sending left trigger value: ", lastLeftTrigger)
                client_UDP.send(str(lastLeftTrigger))
            # Right trigger
            elif event.axis == 5:
                right_trigger_value = round(joystick.get_axis(5),2)
                if lastRightTrigger == None:
                    lastRightTrigger = right_trigger_value
                elif (abs(right_trigger_value - lastRightTrigger) < .05 * 2):
                    continue
                else: 
                    lastRightTrigger = right_trigger_value
                print("Sending right trigger value: ", lastRightTrigger)
                client_UDP.send(str(lastRightTrigger))
            # Left stick
            elif event.axis == 0 or event.axis == 1:
                left_stick_value = int(leftStick.moveStick(joystick.get_axis(0), joystick.get_axis(1)))
                if lastAngle == None:
                    lastAngle = left_stick_value
                elif (abs(left_stick_value - lastAngle) < .05 * 360): #don't send if angle didn't change much
                    continue
                else:
                    lastAngle = left_stick_value
                print(f'Sending angle: {lastAngle}')
                client_UDP.send(str(lastAngle))

    clock.tick(60)