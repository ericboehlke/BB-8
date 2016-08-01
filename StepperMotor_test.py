import Adafruit_BBIO.GPIO as GPIO
import time
from StepperMotor import * 

steppingMode = SteppingMode("P8_10", "P8_11", "P8_12")

motorBlue = StepperMotor("P8_13", "P8_14")
motorGreen = StepperMotor("P9_16", "P8_12")
motorYellow = StepperMotor("P9_28", "P8_10")

steppingMode.setMode(0)

time.sleep(2)

motorBlue.forward(5)
motorGreen.forward(5)
motorYellow.forward(5)

time.sleep(10)

motorBlue.stop()
motorGreen.stop()
motorYellow.stop()