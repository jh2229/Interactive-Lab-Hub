# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from __future__ import print_function

import time
import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility




import qwiic_button
import time
import sys

brightness = 100

from PIL import Image, ImageDraw, ImageFont

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
apds.enable_proximity = True # proximity

my_button = qwiic_button.QwiicButton()


while True:
    my_button.LED_off()
    # wait for color data to be ready
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data

    #temporary holder for light value
    light = colorutility.calculate_lux(r, g, b)
    dist = apds.proximity
    
    
    print("red: ", r)
    print("green: ", g)
    print("blue: ", b)
    print("clear: ", c)

    print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
    time.sleep(0.5)
    
    

    if (light <600) or (apds.proximity > 1):
        my_button.LED_on(brightness)
        

