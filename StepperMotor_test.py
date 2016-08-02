import Adafruit_BBIO.GPIO as GPIO
import time
from StepperMotor import * 

steppingMode = SteppingMode("P9_23", "P9_25", "P9_27")

motorBlue = StepperMotor("P9_22", "P9_24")
motorGreen = StepperMotor("P9_16", "P9_15")
motorYellow = StepperMotor("P9_28", "P9_30")

steppingMode.setMode(5)

motorBlue.forward(3)
motorGreen.forward(10)
motorYellow.forward(20)

time.sleep(10)

motorBlue.stop()
motorGreen.stop()
motorYellow.stop()