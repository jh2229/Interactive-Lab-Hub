import time
from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import math

from adafruit_rgb_display.rgb import color565
import webcolors

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

#Starting Positions of image
#x= 0
#y= 0
temp=0
bd=28 #bar division factor
bs=width/bd # bar separation factor
bh=height/59 # bar height factor


#Button Setup
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

while True & int(strftime("%H%M%S"))!=2355959:
    stnd = int(strftime("%S")) # Hour to be the standard position
    stnd_m = int(strftime("%M"))
    stnd_h = int(strftime("%H"))
    if stnd_h >12:
        stnd_h = stnd_h-12
        color = (100+stnd_h*20, 0, 0) # 1PM-5PM = Red
        if stnd_h > 5:
            color = (0,0,100+stnd_h*20) # 6PM-12AM = Blue
    else:
        color = (0, 100+stnd_h*20, 0) # 1AM-5AM = Green
        if stnd_h> 5:
            color = (100+stnd_h*20, 100+stnd_h*20, 0) #6AM-12PM = Yellow
        
            
    sin_y1= -math.sin(2*3.14/48*int(strftime("%H")))*100+135
    cos_x1= -math.cos(2*3.14/48*int(strftime("%H")))*60+120
    print(cos_x1, sin_y1)
    print(width, height)
    print (strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True)
    print("\r", end="", flush=True)
    #if buttonA.value and buttonB.value:
    #    backlight.value = False  # turn off backlight
    #else:
    #    backlight.value = True  # turn on backlight
    if buttonB.value and not buttonA.value:  # just button A pressed
        #draw.rectangle((0, 0, width, height), outline=0, fill=0)
        while buttonB.value and not buttonA.value: #Visualize Rotating Sun

            draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
            draw.regular_polygon((cos_x1, sin_y1, 30), n_sides=20, rotation =0, fill= (255,0,0), outline=0)
            disp.image(image, rotation)
            
            #print (strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True)
            #print("\r", end="", flush=True)
    if buttonA.value and not buttonB.value:  # just button B pressed
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
            
        draw.text((0, 0), 'Good Morning', font=font, fill="#FFFFFF")
        draw.text((0, font.size), '1. Breakfast', font=font, fill="#FFFFFF")
        draw.text((0, font.size*2), '2. Shower', font=font, fill="#FFFFFF")
        draw.text((0, font.size*3), '3. Shave', font=font, fill="#FFFFFF")
        draw.text((0, font.size*4), '4. Brush Teeth', font=font, fill="#FFFFFF")
        draw.text((0, font.size*5), '5. Go to class', font=font, fill="#FFFFFF")
        disp.image(image, rotation)
    #if not buttonA.value and not buttonB.value:  # none pressed
        #display.fill(color565(0, 255, 0))  # green

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    #draw.rectangle((width-2, 0, width, height), outline=0, fill=color565(0,0,0))
    #disp.fill(color565(255, 255, 255))

    
    if stnd_h > 0:
        draw.rectangle((0, 0, width/bd*2, stnd_m*bh), outline=0, fill= color)
    if stnd_h >1:
        draw.rectangle((width/bd*2, 0, width/bd*4, stnd_m*bh), outline=0, fill=color)
    if stnd_h >2:
        draw.rectangle((width/bd*4, 0, width/bd*6, stnd_m*bh), outline=0, fill=color)
    if stnd_h >3:
        draw.rectangle((width/bd*6, 0, width/bd*8, stnd_m*bh), outline=0, fill=color)
    if stnd_h >4:
        draw.rectangle((width/bd*8, 0, width/bd*10, stnd_m*bh), outline=0, fill=color)
    if stnd_h >5:
        draw.rectangle((width/bd*10+bs, 0, width/bd*12+bs, stnd_m*bh), outline=0, fill=color)
    if stnd_h >6:
        draw.rectangle((width/bd*12+bs, 0, width/bd*14+bs, stnd_m*bh), outline=0, fill=color)
    if stnd_h >7:
        draw.rectangle((width/bd*14+bs, 0, width/bd*16+bs, stnd_m*bh), outline=0, fill=color)
    if stnd_h >8:
        draw.rectangle((width/bd*16+bs, 0, width/bd*18+bs, stnd_m*bh), outline=0, fill=color)        
    if stnd_h >9:
        draw.rectangle((width/bd*18+bs, 0, width/bd*20+bs, stnd_m*bh), outline=0, fill=color)
    if stnd_h >10:
        draw.rectangle((width/bd*20+bs*2, 0, width/bd*22+bs*2, stnd_m*bh), outline=0, fill=color)
    if stnd_h >11:
        draw.rectangle((width/bd*22+bs*2, 0, width/bd*24+bs*2, stnd_m*bh), outline=0, fill=color)
    #if stnd_h >12:
    #    draw.rectangle((width/bd*24+bs*2, 0, width/bd*26+bs*2, stnd_m*bh), outline=0, fill=color) 
    #draw.ellipse([(stnd*4, 135-stnd*2-20),(stnd*4+20, 135-stnd*2)], fill=100, width=20)
    
    #draw.regular_polygon((sin_x1, cos_y1, 30), n_sides=12, rotation =0, fill= stnd*16, outline=0)
    #draw.regular_polygon((stnd*4, 0+stnd_m*5, 10), n_sides=stnd+3, rotation =0, fill= color565(stnd*4,stnd*4,stnd*4), outline=0)
    #draw.regular_polygon((math.sin(2*3.14/120*stnd)*240+67, 0+stnd_m*2, 10), n_sides=stnd+3, rotation =0, fill= color565(stnd*4,stnd*4,stnd*4), outline=0)
    
    #draw.ellipse([(sin_x1,cos_y1),(sin_x1+20, cos_y1+20)], fill=100, width=20)
    #draw.rectangle((0, 0, width, 80), outline=0, fill=50)
    #x+=.01
    #y+=.01
    #temp+=1
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    #print (strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True)
    #print("\r", end="", flush=True)
    if strftime("%H")=="19":
        #print(int(strftime("%H")))
        print(int(strftime("%H%M%S")))
        
    #print (strftime(%m/%d), end="", flush=True)
    #print("\r", end="", flush=True)
    sleep(1)
    
    y = top
    #draw.text((x, y), strftime("%m/%d/%Y %H:%M:%S"), font=font, fill="#FFFFFF")

    #color565(*list(webcolors.name_to_rgb(input('Type the name of a color and hit enter: '))))
    #disp.fill(color565(*list(webcolors.name_to_rgb('yellow'))))

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
while True & int(strftime("%H%M%S"))==000000:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)