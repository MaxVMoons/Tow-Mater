'''
For controlling the drive motor, you will use P9_16.
After powering on the Beagle, toggle the power switch on the car to the on position.
You should hear a quick two beeps followed by a single beep a couple of seconds later.
After you've heard that single beep, you may start controlling the drive motor.

You will again use a frequency of 50Hz.
The motor (technically the ESC) must be initialized before you can drive it.
To to this, you will issue a PWM command with a duty cycle of 7.5%.
You only need to do this once at the beginning and then you can issue forward and reverse throttle commands.

Using Python and the Adafruit BBIO library the initialization sequence would look something like this...

import Adafruit_BBIO.PWM as PWM

PWM.start("P9_16", 0, 50)
PWM.set_duty_cycle("P9_16",7.5)

Full throttle forward is achieved with a duty cycle of 5% while full throttle in reverse is a duty cycle of 10%.
DO NOT EXCEED THESE LIMITS.
Further, you also want to make changes in small steps - I recommend only 0.5% change at a time.
A duty cycle of 7.5% is fully stopped, so I would go from 7.5 -> 7 -> 6.5 ->... as you're accelerating forward.

After initialization, you just need to use the PWM.set_duty_cycle("P9_16",dutyCycle) command

TODO: figure out throttle range for motor by testing on car. Figure out range for no motor movement. Figure out upper and lower bounds for triggers. Boost and reverse boost.
'''

import Adafruit_BBIO.PWM as PWM
import time

servoPin="P9_16"
duty = 0
freq = 50
lastDutyCycle = 7.5

# Translate [-2, 0, 2] to [10, 7.5, 5]
def translateThrottle(inputThrottle):
        global lastDutyCycle
        if inputThrottle == 'BOOST':
                lastDutyCycle -= 0.2
                if lastDutyCycle < 5: lastDutyCycle = 5
        elif inputThrottle == 'REVBOOST':
                lastDutyCycle += 0.2
                if lastDutyCycle > 10: lastDutyCycle = 10
        else:
                scale = 3 #the higher the scale, the lower the range for the throttle
                lastDutyCycle = -(inputThrottle / scale) + 7.5 
        return lastDutyCycle

class Motor(object):
        def __init__(self):
                PWM.start(servoPin, duty, freq)
                PWM.set_duty_cycle("P9_16",7.5)
                lastDutyCycle = 7.5
                
        #auto calibrate the ESC (not needed?)
        def armESC():
                PWM.set_duty_cycle(servoPin, 0.0)
                print("Ensure battery is connected AND switch if OFF. Press ENTER to continue")
                imp = input()
                if imp == '':
                        PWM.set_duty_cycle(servoPin, 10.0)
                        print('Working...')
                        time.sleep(7)
                        print("Wait for it ...")
                        time.sleep(5)
                        print("Almost there . . .")
                        PWM.set_duty_cycle(servoPin, 0.0)
                        time.sleep(2)
                        print("Arming ESC now ...")
                        PWM.set_duty_cycle(servoPin, 10.0)
                        time.sleep(1)
                        print("ESC is arm. Car is ready")
                        PWM.set_duty_cycle(servoPin, 7.5)

        def changeThrottle(self, dutyCycle: float):
                #dutyCycle=float(input("What throttle do You Want (5-10; 7.5 to stop): ")) #debugging
                dutyCycle = round(translateThrottle(dutyCycle), 1)
                PWM.set_duty_cycle(servoPin, dutyCycle)
                print(f'Current dutyCycle for motor: {dutyCycle}')

        def stopMotor(self):
                PWM.stop(servoPin)
                PWM.cleanup()

'''
motor = Motor()
while True:
        motor.changeThrottle(69)
'''