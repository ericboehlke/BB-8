#!/usr/bin/env python

import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from StepperMotor import * 
from termcolor import colored
import math
import threading
from IMU import *
from Omnibot import *
from PID import *
from flask import request, Flask, send_from_directory, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

target = Orientation(5, 0, 0)

@app.route('/tilt')
def tilt ():
    pitch = float(request.args.get('pitch'))
    if pitch > 0:
        pitch = min(pitch, 10)
    else:
        pitch = max(pitch, -10)
    target.pitch = pitch
    
    roll = float(request.args.get('roll'))
    if roll > 0:
        roll = min(roll, 10)
    else:
        roll = max(roll, -10)
    target.roll = roll
    return 'im so cute :)'


twitch = Omnibot()

# twitch.blueWheel.rotate(10)
# sleep(.25)
# twitch.blueWheel.rotate(0)

# twitch.greenWheel.rotate(10)
# sleep(.25)
# twitch.greenWheel.rotate(0)

# twitch.yellowWheel.rotate(10)
# sleep(.25)
# twitch.yellowWheel.rotate(0)

# sleep(5)

imu = IMU(1)
#imu.zero()

twitch.blueWheel.rotate(10)
sleep(.25)
twitch.blueWheel.rotate(0)

twitch.greenWheel.rotate(10)
sleep(.25)
twitch.greenWheel.rotate(0)

twitch.yellowWheel.rotate(10)
sleep(.25)
twitch.yellowWheel.rotate(0)

sleep(1)

zeroAngle = math.radians(180)

def getDriveAngle (x, y, zeroAngle):
	fallingAngle = math.atan2(x, y)
	if fallingAngle < 0:
	    fallingAngle = fallingAngle + 2 * math.pi
	drivingAngle = fallingAngle + math.pi + zeroAngle
	if drivingAngle > 2 * math.pi:
	    drivingAngle = drivingAngle - 2 * math.pi
	return drivingAngle
	
def getDriveSpeed (x, y):
    drivingSpeed = 200 * (x ** 2 + y ** 2) ** (.5) 
    return drivingSpeed
    
#pitch = []
#roll = []
pitchPIDController = PIDController()
rollPIDController = PIDController()
#count = 0
def balance():
    while True:
        startTime = time.time()
        orientation = imu.getOrientation()
        orientation.pitch = orientation.pitch - target.pitch
        orientation.roll = orientation.roll - target.roll
        driveAngle = getDriveAngle(math.radians(orientation.roll), math.radians(orientation.pitch), zeroAngle)
        print target.pitch, target.roll
        driveSpeedY = pitchPIDController.calculateSpeed(0, orientation.pitch)
        driveSpeedX = rollPIDController.calculateSpeed(0, orientation.roll)
        # print "speedX:", driveSpeedX, "speedY:", driveSpeedY
        driveSpeed = (driveSpeedX ** 2 + driveSpeedY ** 2) ** (.5)
        driveSpeed = min(driveSpeed, 100)
        twitch.move(driveAngle, driveSpeed)
    
        #count = count + 1
        #pitch.append(orientation.pitch)
        #roll.append(orientation.roll)
        
        # print colored('----------------------------------','cyan')	
        # print colored('roll = {0:.2f}, pitch = {1:.2f}','white') .format(orientation.roll, orientation.pitch)
        # print "direction:", driveAngle, "speed:", driveSpeed
        #print "PID useful time:", (time.time() - startTime)
        sleep(max(.05 - (time.time() - startTime), 0))
        #print "PID controller loop time:", time.time() - startTime
    
# twitch.stop()
# def average(s): return sum(s) * 1.0 / len(s)

# avgPitch = average(pitch)
# avgRoll = average(roll)
# variancePitch = map(lambda x: (x - avgPitch)**2, pitch)
# varianceRoll = map(lambda x: (x - avgRoll)**2, roll)
# print colored('----------------------------------','cyan')	
# print colored('----------------------------------','cyan')	
# print 'mean: ', avgPitch, avgRoll
# print 'average variance: ', average(variancePitch), average(varianceRoll)

thread = threading.Thread(target=balance)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(host = '0.0.0.0',
            port = 5000)
