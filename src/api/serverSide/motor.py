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

TODO: figure out range for motor 
'''

import Adafruit_BBIO.PWM as PWM

servoPin="P9_16"
duty = 0 # initial value
freq = 50

class Motor(object):
        def __init__(self):
                PWM.start(servoPin, duty, freq)

        def changeThrottle(self, desiredThrottle: float):
                #desiredThrottle=float(input("What throttle do You Want: "))
                dutyCycle= 1/18*desiredThrottle + 2
                PWM.set_duty_cycle(servoPin, dutyCycle)
                print("Current dutyCycle", dutyCycle)