# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility



import board
import busio
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
apds.enable_proximity = True # proximity

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


# Helper function to draw a circle from a given position with a given radius
# This is an implementation of the midpoint circle algorithm,
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example for details
def draw_circle(xpos0, ypos0, rad, col=1):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        oled.pixel(xpos0 + x, ypos0 + y, col)
        oled.pixel(xpos0 + y, ypos0 + x, col)
        oled.pixel(xpos0 - y, ypos0 + x, col)
        oled.pixel(xpos0 - x, ypos0 + y, col)
        oled.pixel(xpos0 - x, ypos0 - y, col)
        oled.pixel(xpos0 - y, ypos0 - x, col)
        oled.pixel(xpos0 + y, ypos0 - x, col)
        oled.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)


# initial center of the circle
center_x = 63
center_y = 15
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 8

# start with a blank screen
oled.fill(0)


# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)



# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
oled.show()



while True:
    
    # Clear display.
    #oled.fill(0)
    oled.show()
    # create some variables to store the color data in
    
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
    
    
    # Draw the text
    draw.text((0, 0), "Blinks if too dark", font=font2, fill=255)
    draw.text((0, 13), "Blinks if too close".format(dist), font=font2, fill=255)
    


    # Display image
    oled.image(image)
    oled.show()

    # Clear display.
    #draw.text((0, 0), "light lux {}".format(light), font=font2, fill=0)
    draw.text((0, 0), "Blinks if too dark", font=font2, fill=0)
    draw.text((0, 13), "Blinks if too close", font=font2, fill=0)

    if (light <600) & (apds.proximity > 1):
        #draw.rectangle((0, 0, 128, 16), outline=255, fill=255)
        oled.fill(0)
    #if apds.proximity > 1:
     #   draw.rectangle((0, 17, 128, 32), outline=125, fill=125)
    
    
    oled.show()
    #oled.image(image)
    #draw.rectangle((0, 0, 128, 16), outline=0, fill=0)
    #draw.rectangle((0, 17, 128, 32), outline=0, fill=0)
    #draw.text((0, 0), "Lights if too dark", font=font2, fill=255)
    #draw.text((0, 13), "Lights if too close".format(dist), font=font2, fill=255)
    #draw.rectangle((0, 0, 128, 32), outline=0, fill=0)

        #draw.rectangle((0, 0, 128, 16), outline=0, fill=0)
        #oled.show()


        
        


        #draw.rectangle((0, 17, 128, 32), outline=0, fill=0)
        #oled.show()
    
