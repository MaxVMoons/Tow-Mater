import Adafruit_BBIO.PWM as PWM

# Use a frequency of 50Hz and then a duty cycle range of 5% to 10%. You will want to gradually steer the car using duty cycle values between these two limits.
# Valid angles: 1.2 -195.3

servoPin="P9_14"
duty = 8.25 # prev was 2, initial value
freq = 50

class Steering(object):
        def __init__(self):
                PWM.start(servoPin, duty, freq)
        
        def changeAngle(self, desiredAngle: float):
                # desiredAngle=float(input("What Angle do You Want: "))
                dutyCycle= 1/18*desiredAngle + 2
                PWM.set_duty_cycle(servoPin, dutyCycle)