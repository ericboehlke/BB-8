import time
import math
from Omnibot import * 

zeroAngle = math.radians(103)

twitch = Omnibot()
twitch.move(90, 20)

time.sleep(5)

twitch.stop()