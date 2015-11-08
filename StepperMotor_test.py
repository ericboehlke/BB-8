import Adafruit_BBIO.GPIO as GPIO
import time
from StepperMotor import * 

motorYellow = StepperMotor("P9_21", "P9_23", "P9_16", "P9_25", "P9_27", "P9_22", StepperMotor.MICRO_STEP)
motorGreen = StepperMotor("P8_8", "P8_10", "P8_19", "P8_12", "P8_14", "P8_13", StepperMotor.MICRO_STEP)
motorBlue = StepperMotor("P9_24", "P9_26", "P9_42", "P9_30", "P9_41", "P9_28", StepperMotor.MICRO_STEP)

motorBlue.forward(5)
motorYellow.forward(5)
motorGreen.forward(5)
time.sleep(1)
motorBlue.stop()
motorYellow.stop()
motorGreen.stop()

while True:
    time.sleep(5)



