from StepperMotor import * 
import math

class Omniwheel(object):
    
    def __init__ (self, pin1, pin2, pwmA, pin3, pin4, pwmB, steppingMode, wheelAngle):
        self.motor = StepperMotor(pin1, pin2, pwmA, pin3, pin4, pwmB, steppingMode)
        self.wheelAngle = wheelAngle
    
    def calculateVelocity (self, drivingAngle, drivingSpeed): 
        w = self.wheelAngle
        d = drivingAngle
        wheelSpeed = drivingSpeed * (math.cos(w) * math.cos(d) + math.sin(w) * math.sin(d))
        if wheelSpeed > 0:
            self.motor.forward(wheelSpeed)
        else:
            self.motor.reverse(abs(wheelSpeed))
            
        
class Omnibot(object):
    
    def __init__ (self):
        self.blueWheel = Omniwheel("P9_24", "P9_26", "P9_42", "P9_30", "P9_41", "P9_28", StepperMotor.MICRO_STEP, math.radians(0))
        self.yellowWheel = Omniwheel("P9_21", "P9_23", "P9_16", "P9_25", "P9_27", "P9_22", StepperMotor.MICRO_STEP, math.radians(120))
        self.greenWheel = Omniwheel("P8_8", "P8_10", "P8_19", "P8_12", "P8_14", "P8_13", StepperMotor.MICRO_STEP, math.radians(240))

    def move (self, angle, speed):
        self.blueWheel.calculateVelocity(angle, speed)
        self.yellowWheel.calculateVelocity(angle, speed)
        self.greenWheel.calculateVelocity(angle, speed)
        
    def stop (self):
        self.blueWheel.motor.stop()
        self.yellowWheel.motor.stop()
        self.greenWheel.motor.stop()