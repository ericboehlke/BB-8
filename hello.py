import time
import math
from flask import request, Flask, send_from_directory
from Omnibot import *
app = Flask(__name__)

twitch = Omnibot()

@app.route('/')
def hello():
    return send_from_directory('html','index.html')

@app.route('/move')
def move ():
  direction, speed = float(request.args.get('direction')), float(request.args.get('speed'))
  twitch.move(math.radians(direction), speed)
  return 'hooray'
  
@app.route('/spin')
def spin ():
  speed = float(request.args.get('speed'))
  twitch.spin(speed)
  return 'dizzy'
  
@app.route('/stop')
def halt ():
  twitch.stop()
  return 'bored'
  
@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('js', path)
  
@app.route('/images/<path:path>')
def send_image(path):
  return send_from_directory('images', path)
  
@app.route('/control')
def touchController():
  return send_from_directory('html', 'TouchControl.html')
  
if __name__ == '__main__':
    app.run(host = '0.0.0.0',
            port = 5000)