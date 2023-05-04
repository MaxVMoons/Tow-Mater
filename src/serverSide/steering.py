import Adafruit_BBIO.PWM as PWM

'''
Use a frequency of 50Hz and then a duty cycle range of 5% to 10%. 
You will want to gradually steer the car using duty cycle values between these two limits.
Valid angles for RC car in mix: 140 is max. 0-40 is min . . . in terms of dutyCycle: 4.2-9.8
'''

servoPin="P9_14"
duty = 8.2 # initial position for the steering. TODO: 8.2 vs 7.5. Figure out what is centered and if the wheels respond outside [5, 10]
freq = 50

#inputAngle is 0-180. Put in suggested dutyCycle for servo.
def getDutyCycle(inputAngle):
        newAngleMin = 5
        newAngleMax = 10
        # Map the angle to the valid angle range
        return (inputAngle / 180.0) * (newAngleMax - newAngleMin) + newAngleMin
        
class Steering(object):
        def __init__(self):
                PWM.start(servoPin, duty, freq)
        
        def changeAngle(self, desiredAngle: float):
                #desiredAngle=float(input("What Angle do You Want: ")) #debugging
                dutyCycle = round(getDutyCycle(desiredAngle), 1)
                #dutyCycle= 1/18*desiredAngle + 2 #converts angle to dutyCycle.
                PWM.set_duty_cycle(servoPin, dutyCycle)
                print(f'Current dutyCycle for steering: {dutyCycle}')
        
        def stopMotor(self):
                PWM.stop(servoPin)
                PWM.cleanup()

'''
steering = Steering()
while True:
        steering.changeAngle(69.9)
'''     