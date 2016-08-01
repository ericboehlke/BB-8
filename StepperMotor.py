import Adafruit_BBIO.GPIO as GPIO
import time
import threading
import math
import Adafruit_BBIO.PWM as PWM

class SteppingMode:
    
    class __SteppingMode:
        def __init__(self, m0, m1, m2):
            GPIO.setup(m0, GPIO.OUT)
            GPIO.setup(m1, GPIO.OUT)
            GPIO.setup(m2, GPIO.OUT)
            self.m0 = m0
            self.m1 = m1
            self.m2 = m2
    
    instance = None
    
    def __init__(self, m0, m1, m2):
        if not SteppingMode.instance:
            SteppingMode.instance = SteppingMode.__SteppingMode(m0, m1, m2)
    
    def setMode(self, mode):
        SteppingMode.instance.mode = mode
        GPIO.output(SteppingMode.instance.m0, mode & 1 == 1) 
        GPIO.output(SteppingMode.instance.m1, mode & 2 == 2) 
        GPIO.output(SteppingMode.instance.m2, mode & 4 == 4) 
       
    @staticmethod    
    def getFrequency(rpm):
        if SteppingMode.instance.mode > 5:
            mode = 5
        else: 
            mode = SteppingMode.instance.mode
        return rpm * 200 * (2 ** mode) / 60
        
class StepperMotor(object):
    
    def __init__ (self, stepPin, directionPin):
        GPIO.setup(directionPin, GPIO.OUT)
        self.stepPin = stepPin
        self.directionPin = directionPin
        
    def setSpeed(self, rpm):
        if rpm != 0:
            PWM.start(self.stepPin, 50, SteppingMode.getFrequency(rpm), 1)
        else:
            PWM.stop(self.stepPin)
        print SteppingMode.getFrequency(rpm)

    def forward(self, rpm):
        GPIO.output(self.directionPin, GPIO.HIGH)
        self.setSpeed(rpm)

    def reverse(self, rpm):
        GPIO.output(self.directionPin, GPIO.LOW)
        self.setSpeed(rpm)

    def stop(self):
        PWM.stop(self.stepPin)