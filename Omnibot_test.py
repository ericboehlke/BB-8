import time
import math
from Omnibot import * 

zeroAngle = math.radians(103)

twitch = Omnibot()
twitch.move(-30, 40)

time.sleep(.25)

twitch.spin(40)

time.sleep(.5)

twitch.spin(0)

time.sleep(2)

twitch.spin(-10)

time.sleep(2)

twitch.stop()