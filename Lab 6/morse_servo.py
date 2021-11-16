import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# There are 16 channels on the PCA9685 chip.
kit = ServoKit(channels=16)

# Name and set up the servo according to the channel you are using.
servo = kit.servo[2]

# Set the pulse width range of your servo for PWM control of rotating 0-180 degree (min_pulse, max_pulse)
# Each servo might be different, you can normally find this information in the servo datasheet
#servo.set_pulse_width_range(500, 2500)

class Servo:
	def __init__(self, servo):
		self.angle = 0
		self.servo = servo
	
	def dot(self):
		if (self.angle == 180):
			self.angle = 0
			self.servo.angle = self.angle
		else:
			self.angle = 180
			self.servo.angle = self.angle
	
	#def dash(self):
	#	if (self.angle 180):
			

def dot():
	if (servo.angle == 180):
		servo.angle = 0
	else: 
		servo.angle = 180

def dash():
	dot()
	time.sleep(.25)
	dot()
	time.sleep(.25)
	

while True:
    try:
        # Set the servo to 180 degree position
        #servo.angle = 180
        #kit.continuous_servo[0].throttle = 1
        dot()
        time.sleep(2)
        # Set the servo to 0 degree position
        #kit.continuous_servo[0].throttle = -1
        dash()
        time.sleep(2)
        #kit.continuous_servo[0].throttle = 0
        dot()
        time.sleep(2)
        
    except KeyboardInterrupt:
        # Once interrupted, set the servo back to 0 degree position
        servo.angle = 0
        time.sleep(0.5)
        break
