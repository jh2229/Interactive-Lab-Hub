from __future__ import print_function
import qwiic_joystick
import time
import sys
import subprocess
import digitalio

import board
import busio
import paho.mqtt.client as mqtt
import uuid

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
bigfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

received=''

# the # wildcard means we subscribe to all subtopics of IDD
topic = 'IDD/morse'

# some other examples
# topic = 'IDD/a/fun/topic'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')

# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	received = received + msg.payload.decode('UTF-8')
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing


client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/MorseCode/DeviceInput'

i2c = busio.I2C(board.SCL, board.SDA)

print("\nSparkFun qwiic Joystick   Example 1\n")
myJoystick = qwiic_joystick.QwiicJoystick()

if myJoystick.connected == False:
	print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
		file=sys.stderr)

myJoystick.begin()
temp=' '
sent=''

print("Initialized. Firmware Version: %s" % myJoystick.version)

while True:

	print("X: %d, Y: %d, Button: %d" % ( \
				myJoystick.horizontal, \
				myJoystick.vertical, \
				myJoystick.button))

	val = ' '
	if (myJoystick.horizontal in range(600, 1100)) & (myJoystick.vertical in range(400, 600)):
		val = 'up'
		temp = temp+'_'
		print(temp)        
	elif (myJoystick.horizontal in range(400, 600)) & (myJoystick.vertical in range(0, 100)):
		val = 'backspace'
		if not (len(temp) == 0):
			temp = temp[0:len(temp) - 1]
		#temp = '<-'
		print('backspace')
	elif (myJoystick.horizontal in range(400, 600)) & (myJoystick.vertical in range(900, 1100)):
		val = 'right'
		print('right')
	elif (myJoystick.horizontal in range(0, 100)) & (myJoystick.vertical in range(400, 600)):
		val = 'down'
		temp = temp+'.'
		print(temp)
	
	#if temp == 'ls':
		            
	#val = myJoystick.horizontal | myJoystick.
	if myJoystick.button == 0:
		if temp == '':
			client.publish(topic, ' ')    
		else:
			client.publish(topic, temp)
		print('Printed')
		sent = sent + temp
		temp=''

	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	y = top
	current_morse = "Current letter: "
	draw.text((x, y), current_morse, font=font, fill="#FFFFFF")
	y += font.getsize(current_morse)[1]
	draw.text((x, y), temp, font=font, fill="#FFFFFF")
	y += font.getsize(current_morse)[1]
	draw.text((x, y), 'Sent: ' + sent, font=font, fill="#FFFFFF")
	y += font.getsize(current_morse)[1]
	draw.text((x, y), 'Received: ' + received, font=font, fill="#FFFFFF")
	disp.image(image, rotation)
	time.sleep(.5)
