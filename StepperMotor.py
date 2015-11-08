import Adafruit_BBIO.GPIO as GPIO
import time
import threading
import math
import Adafruit_BBIO.PWM as PWM

class StepperCoil(object):
    
    def __init__ (self, pin1, pin2, pwm):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pwm = pwm
        self.direction = "undefined"
        
    def setPower(self, power):
        if power < 0:
            self.pull(abs(power))
        else:
            self.push(power)
    
    def push(self, power = 100):
        if self.direction != "push":
            GPIO.output(self.pin1, GPIO.HIGH)
            GPIO.output(self.pin2, GPIO.LOW)
            self.direction = "push"
        PWM.set_duty_cycle(self.pwm, power)
    
    def pull(self, power = 100):
        if self.direction != "pull":
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.HIGH)
            self.direction = "pull"
        PWM.set_duty_cycle(self.pwm, power)
    
    def off(self):
        if self.direction != "off":
            GPIO.output(self.pin1, GPIO.LOW)
            GPIO.output(self.pin2, GPIO.LOW)
            self.direction = "off"

class StepperMotor(object):
    
    MICRO_STEP = 18000
    HALF_STEP = 400
    FULL_STEP = 200
    
    def __init__ (self, pin1, pin2, pwmA, pin3, pin4, pwmB, steppingMode):
        GPIO.setup(pin1, GPIO.OUT)
        GPIO.setup(pin2, GPIO.OUT)
        GPIO.setup(pin3, GPIO.OUT)
        GPIO.setup(pin4, GPIO.OUT)
        # PWM.start(pwmA)
        # PWM.start(pwmB)
        if (pwmA == 'P8_19'):
            PWM.start(pwmA)
        else:
            PWM.start(pwmA, 0, 500000, 0)
        if (pwmB == 'P8_13'):
            PWM.start(pwmB)
        else:
            PWM.start(pwmB, 0, 500000, 0)
        self.coilA = StepperCoil(pin1, pin2, pwmA)
        self.coilB = StepperCoil(pin3, pin4, pwmB)
        self.step = 0
        self.delay = 0
        self.rpm = 0
        self.direction = 0
        self.stepsPerRevolution = steppingMode
        self.fullSteps = {
            0 : self.step1,
            1 : self.step3,
            2 : self.step5,
            3 : self.step7
        }
        self.halfSteps = {
            0 : self.step1,
            1 : self.step2,
            2 : self.step3,
            3 : self.step4,
            4 : self.step5,
            5 : self.step6,
            6 : self.step7,
            7 : self.step8
        }
        
        if steppingMode == StepperMotor.MICRO_STEP:
            self.thread = threading.Thread(target=self.microStep)
        elif steppingMode == StepperMotor.HALF_STEP:
            self.thread = threading.Thread(target=self.halfStep)
        else:
            self.thread = threading.Thread(target=self.fullStep)
        
        self.isRunning = True
        self.thread.daemon = True
        self.thread.start()
    
    def setSpeed(self, rpm):
        self.rpm = rpm
        if rpm == 0 :
            self.delay = 1000
        else:
            self.delay = 60.0 / self.stepsPerRevolution / rpm

    def forward(self, rpm):
        self.direction = 1
        self.setSpeed(rpm)

    def reverse(self, rpm):
        self.direction = -1
        self.setSpeed(rpm)

    def stop(self):
        self.isRunning = False
        self.coilA.off()
        self.coilB.off()
    
    def microStep(self):
        while self.isRunning:
            angle = math.radians(self.step)
            self.coilA.setPower(math.cos(angle)*100)
            self.coilB.setPower(math.sin(angle)*100)
            self.step = ((self.step + (self.direction * self.rpm)) % 360 + 360) % 360
            startTime = time.time()
            while ((time.time() - startTime < self.delay * self.rpm) & self.isRunning):
                time.sleep(60.0 / self.stepsPerRevolution * self.rpm / 50)

    def halfStep(self):
        while self.isRunning:
            self.halfSteps[self.step]()
            self.step = ((self.step + self.direction) % 8 + 8) % 8
            startTime = time.time()
            while ((time.time() - startTime < self.delay) & self.isRunning):
                time.sleep(60.0 / self.stepsPerRevolution / 50)

    def fullStep(self):
        while self.isRunning:
            self.fullSteps[self.step]()
            self.step = ((self.step + self.direction) % 4 + 4) % 4
            startTime = time.time()
            while ((time.time() - startTime < self.delay) & self.isRunning):
                time.sleep(60.0 / self.stepsPerRevolution / 50)

    def step1(self):
        self.coilA.pull()
        self.coilB.off()

    def step2(self):
        self.coilA.pull()
        self.coilB.pull()

    def step3(self):
        self.coilA.off()
        self.coilB.pull()

    def step4(self):
        self.coilA.push()
        self.coilB.pull()

    def step5(self):
        self.coilA.push()
        self.coilB.off()
        
    def step6(self):
        self.coilA.push()
        self.coilB.push()
    
    def step7(self):
        self.coilA.off()
        self.coilB.push()
    
    def step8(self):
        self.coilA.pull()
        self.coilB.push()
