import time
import math
from Omnibot import * 

zeroAngle = math.radians(103)

twitch = Omnibot()
<<<<<<< Updated upstream
for direction in range(0, 360, 10):
    twitch.move(math.radians(direction), 5)
    time.sleep(.5)
    print math.radians(direction)
=======
# twitch.move(-30, 40)
>>>>>>> Stashed changes

time.sleep(.25)

twitch.spin(40)

time.sleep(2)

twitch.spin(0)

time.sleep(2)

twitch.spin(-10)

time.sleep(2)

twitch.stop()