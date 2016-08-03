from StepperMotor import * 
import math

class Omniwheel(object):
    
    def __init__ (self, stepPin, directionPin, wheelAngle):
        self.motor = StepperMotor(stepPin, directionPin)
        self.wheelAngle = wheelAngle
    
    def calculateVelocity (self, drivingAngle, drivingSpeed): 
        w = self.wheelAngle
        d = drivingAngle
        wheelSpeed = drivingSpeed * (math.cos(w) * math.cos(d) + math.sin(w) * math.sin(d))
        if wheelSpeed > 0:
            self.motor.forward(wheelSpeed)
        else:
            self.motor.reverse(abs(wheelSpeed))
            
    def rotate (self, speed):
        if speed >= 0:
            self.motor.forward(speed)
        else:
            self.motor.reverse(abs(speed))
            
class Omnibot(object):
    
    def __init__ (self):
        self.blueWheel = Omniwheel("P9_22", "P9_24", math.radians(0))
        self.yellowWheel = Omniwheel("P8_13", "P8_14", math.radians(120))
        self.greenWheel = Omniwheel("P9_16", "P9_15", math.radians(240))
        self.steppingMode = SteppingMode("P9_23", "P9_25", "P9_27")
        self.steppingMode.setMode(5)

    def move (self, angle, speed):
        self.blueWheel.calculateVelocity(angle, speed)
        self.yellowWheel.calculateVelocity(angle, speed)
        self.greenWheel.calculateVelocity(angle, speed)
        
    def spin (self, speed):
        self.blueWheel.rotate(speed)
        self.yellowWheel.rotate(speed)
        self.greenWheel.rotate(speed)
        
    def stop (self):
        self.blueWheel.motor.stop()
        self.yellowWheel.motor.stop()
        self.greenWheel.motor.stop()