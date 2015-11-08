import time
import math
from Omnibot import * 


twitch = Omnibot()
twitch.move(math.radians(77), 2)
time.sleep(2)

while True:
    #twitch.move(math.radians(77), 2)
    time.sleep(60.0 / 400 / 50)
