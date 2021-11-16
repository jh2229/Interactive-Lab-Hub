from __future__ import print_function
import qwiic_joystick
import time
import sys

import board
import busio
import paho.mqtt.client as mqtt
import uuid


client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/MorseCode/DeviceInput'

i2c = busio.I2C(board.SCL, board.SDA)

def runExample():

	print("\nSparkFun qwiic Joystick   Example 1\n")
	myJoystick = qwiic_joystick.QwiicJoystick()

	if myJoystick.connected == False:
		print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myJoystick.begin()
	temp=' '
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
			temp = '<-'
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
			temp=''
		time.sleep(.5)

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)